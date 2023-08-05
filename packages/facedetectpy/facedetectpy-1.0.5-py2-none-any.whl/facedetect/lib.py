#!/usr/bin/env python3
# facedetect: a simple face detector for batch processing
# Copyright(c) 2013-2017 by wave++ "Yuri D'Elia" <wavexx@thregr.org>
# Distributed under GPLv2+ (see COPYING) WITHOUT ANY WARRANTY.
from __future__ import print_function, division, generators, unicode_literals

import argparse
import numpy as np
import cv2
import math
import sys
import os

class FaceDetector(object):
    def __init__(self, config=None):
        # Profiles
        self._configuration = {}
        self._configuration['DATA_DIR'] = '/usr/share/opencv/'
        self._configuration['CASCADES'] = {}

        self._configuration['PROFILES'] = {
            'HAAR_FRONTALFACE_ALT2': 'haarcascades/haarcascade_frontalface_alt2.xml',
        }

        # Face normalization
        self._configuration['NORM_SIZE'] = 100
        self._configuration['NORM_MARGIN'] = 10

    def configure(self, config=None):
        if isinstance(config, dict):
            self._configuration.update(config)

        self._cv2_compatibility()
        self._load_cascades(self._configuration['DATA_DIR'])

    def get_config(self):
        return self._configuration

    def _cv2_compatibility(self):
        # CV compatibility stubs
        if 'IMREAD_GRAYSCALE' not in dir(cv2):
            # <2.4
            cv2.IMREAD_GRAYSCALE = 0
        if 'cv' in dir(cv2):
            # <3.0
            cv2.CASCADE_DO_CANNY_PRUNING = cv2.cv.CV_HAAR_DO_CANNY_PRUNING
            cv2.CASCADE_FIND_BIGGEST_OBJECT = cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT
            cv2.FONT_HERSHEY_SIMPLEX = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX,
                                                       0.5, 0.5, 0, 1, cv2.cv.CV_AA)
            cv2.LINE_AA = cv2.cv.CV_AA

            def _getTextSize(buf, font, scale, thickness):
                return cv2.cv.GetTextSize(buf, font)

            def _putText(im, line, pos, font, scale, color, thickness, lineType):
                return cv2.cv.PutText(cv2.cv.fromarray(im), line, pos, font, color)

            cv2.getTextSize = _getTextSize
            cv2.putText = _putText

    # Support functions
    def error(self, msg):
        sys.stderr.write("{}: error: {}\n".format(os.path.basename(sys.argv[0]), msg))


    def fatal(self, msg):
        self.error(msg)
        sys.exit(1)


    def _load_cascades(self, data_dir):
        for k, v in self._configuration['PROFILES'].items():
            v = os.path.join(data_dir, v)
            try:
                if not os.path.exists(v):
                    raise cv2.error('no such file')
                self._configuration['CASCADES'][k] = cv2.CascadeClassifier(v)
            except cv2.error:
                self.fatal("cannot load {} from {}".format(k, v))


    def _crop_rect(self, im, rect, shave=0):
        return im[rect[1]+shave:rect[1]+rect[3]-shave, rect[0]+shave:rect[0]+rect[2]-shave]


    def _shave_margin(self, im, margin):
        return im[margin:-margin, margin:-margin]


    def _norm_rect(self, im, rect, equalize=True, same_aspect=False):
        roi = self._crop_rect(im, rect)
        if equalize:
            roi = cv2.equalizeHist(roi)
        side = self._configuration['NORM_SIZE'] + self._configuration['NORM_MARGIN']
        if same_aspect:
            scale = side / max(rect[2], rect[3])
            dsize = (int(rect[2] * scale), int(rect[3] * scale))
        else:
            dsize = (side, side)
        roi = cv2.resize(roi, dsize, interpolation=cv2.INTER_CUBIC)
        return self._shave_margin(roi, self._configuration['NORM_MARGIN'])


    def _rank(self, im, rects):
        scores = []
        best = None

        for i in range(len(rects)):
            rect = rects[i]
            roi_n = self._norm_rect(im, rect, equalize=False, same_aspect=True)
            roi_l = cv2.Laplacian(roi_n, cv2.CV_8U)
            e = np.sum(roi_l) / (roi_n.shape[0] * roi_n.shape[1])

            dx = im.shape[1] / 2 - rect[0] + rect[2] / 2
            dy = im.shape[0] / 2 - rect[1] + rect[3] / 2
            d = math.sqrt(dx ** 2 + dy ** 2) / (max(im.shape) / 2)

            s = (rect[2] + rect[3]) / 2
            scores.append({'s': s, 'e': e, 'd': d})

        sMax = max([x['s'] for x in scores])
        eMax = max([x['e'] for x in scores])

        for i in range(len(scores)):
            s = scores[i]
            sN = s['sN'] = s['s'] / sMax
            eN = s['eN'] = s['e'] / eMax
            f = s['f'] = eN * 0.7 + (1 - s['d']) * 0.1 + sN * 0.2

        ranks = range(len(scores))
        ranks = sorted(ranks, reverse=True, key=lambda x: scores[x]['f'])
        for i in range(len(scores)):
            scores[ranks[i]]['RANK'] = i

        return scores, ranks[0]


    def _mssim_norm(self, X, Y, K1=0.01, K2=0.03, win_size=11, sigma=1.5):
        C1 = K1 ** 2
        C2 = K2 ** 2
        cov_norm = win_size ** 2

        ux = cv2.GaussianBlur(X, (win_size, win_size), sigma)
        uy = cv2.GaussianBlur(Y, (win_size, win_size), sigma)
        uxx = cv2.GaussianBlur(X * X, (win_size, win_size), sigma)
        uyy = cv2.GaussianBlur(Y * Y, (win_size, win_size), sigma)
        uxy = cv2.GaussianBlur(X * Y, (win_size, win_size), sigma)
        vx = cov_norm * (uxx - ux * ux)
        vy = cov_norm * (uyy - uy * uy)
        vxy = cov_norm * (uxy - ux * uy)

        A1 = 2 * ux * uy + C1
        A2 = 2 * vxy + C2
        B1 = ux ** 2 + uy ** 2 + C1
        B2 = vx + vy + C2
        D = B1 * B2
        S = (A1 * A2) / D

        return np.mean(self._shave_margin(S, (win_size - 1) // 2))

    def _pairwise_similarity(self, im, features, template, **mssim_args):
        template = np.float32(template) / 255
        for rect in features:
            roi = self._norm_rect(im, rect)
            roi = np.float32(roi) / 255
            yield self._mssim_norm(roi, template, **mssim_args)

    def detect(self, im, biggest=False):
        side = math.sqrt(im.size)
        minlen = int(side / 20)
        maxlen = int(side / 2)
        flags = cv2.CASCADE_DO_CANNY_PRUNING

        # optimize queries when possible
        if biggest:
            flags |= cv2.CASCADE_FIND_BIGGEST_OBJECT

        # frontal faces
        cc = self._configuration['CASCADES']['HAAR_FRONTALFACE_ALT2']
        features = cc.detectMultiScale(im, 1.1, 4, flags, (minlen, minlen), (maxlen, maxlen))
        return features


    def detect_from_file(self, path, biggest=False):
        im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if im is None:
            self.fatal("cannot load input image {}".format(path))
        im = cv2.equalizeHist(im)
        features = self.detect(im, biggest)
        return im, features

    def detect_similar_faces(self, path, source_image, search_threshold=30, debug=False):
        im, features = self.detect_from_file(path)
        s_im, s_features = self.detect_from_file(source_image, True) # match against biggest file.
        if len(s_features) == 0:
            self.fatal("cannot detect face in source template")
        sim_scores = []
        sim_features = []
        sim_threshold = search_threshold / 100
        sim_template = self._norm_rect(s_im, s_features[0])
        for i, score in enumerate(self._pairwise_similarity(im, features, sim_template)):
            if score >= sim_threshold:
                sim_scores.append(score)
                sim_features.append(features[i])

        return im, sim_features, sim_scores

    def debug_info(self, img_features, sim_scores=None):
        # compute scores
        img, features = img_features
        scores = []
        best = None
        if len(features):
            scores, best = self._rank(img, features)
            if sim_scores:
                for i in range(len(features)):
                    scores[i]['MSSIM'] = sim_scores[i]

        return scores, best

    def output_to_file(self, img_features, outfile, best=None, debug_scores=None):
        img, features = img_features
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_height = cv2.getTextSize("", font, 0.5, 1)[0][1] + 5

        white = (255, 255, 255)
        yellow = (0, 255, 255)

        def draw_rectangle(rect, line_color):
            xy1 = (rect[0], rect[1])
            xy2 = (rect[0] + rect[2], rect[1] + rect[3])
            cv2.rectangle(img, xy1, xy2, (0, 0, 0), 4)
            cv2.rectangle(img, xy1, xy2, line_color, 2)

        def draw_debug(rect, rect_scores, line_color):
            lines = []
            for key, val in rect_scores.items():
                lines.append("SCORE {}: {}".format(key, val))
            height = rect[1] + rect[3] + font_height
            for line in lines:
                cv2.putText(img, line, (rect[0], height), font, 0.5, line_color, 1, cv2.LINE_AA)
                height += font_height

        for idx, rect in enumerate(features):
            if best is not None and idx != best and not debug_scores:
                continue

            line_color = yellow if idx == best else white
            draw_rectangle(rect, line_color)

            if debug_scores:
                draw_debug(rect, debug_scores[idx], line_color)

        cv2.imwrite(outfile, img)

    def get_center(self, rect):
        x = int(rect[0] + rect[2] / 2)
        y = int(rect[1] + rect[3] / 2)
        return x, y

