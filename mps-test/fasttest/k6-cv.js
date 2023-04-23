import http from 'k6/http';
import encoding from 'k6/encoding';
import { group } from 'k6'
import { check, sleep } from 'k6';
import { Trend } from 'k6/metrics';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';


export const options = {
  scenarios: {
    resnet_test: {
      executor: 'constant-vus',
      startTime: '0s',
      vus: 15,
      duration: '10m',
      gracefulStop: '1s', // do not wait for iterations to finish in the end
      tags: { test_type: 'resnet' }, // extra tags for the metrics generated by this scenario
      exec: 'resnet_func', // the function this scenario will execute
    },
    rnnt_test: {
      executor: 'constant-vus',
      startTime: '2.5m',
      vus: 15,
      duration: '5m',
      gracefulStop: '1s', // do not wait for iterations to finish in the end
      tags: { test_type: 'rnnt' }, // extra tags for the metrics generated by this scenario
      exec: 'rnnt_func', // the function this scenario will execute
    },
  },
  discardResponseBodies: true,
  thresholds: {
    'http_reqs{test_type:resnet}': [],
    'http_reqs{test_type:rnnt}': [],
  },
};

let gateway = "http://10.108.101.210:8080"

const image = open('car.jpg', 'b');
const fd = new FormData();
fd.append('payload', http.file(image, 'image.png', 'image/png'));
let resnet = {
        method: 'POST',
        url: gateway + '/function/resnet/predict',
        body: fd.body(),
        params: {
            headers: {
              'Content-Type': 'multipart/form-data; boundary=' + fd.boundary
            },
        },
};

const wavefile = open('en.wav', 'b');
const fdwav = new FormData();
fdwav.append('payload', http.file(wavefile, 'en.wav'));
let rnnt = {
        method: 'POST',
        //url: "http://10.244.0.81:8080/predict",
	url: gateway + '/function/rnnt/predict',
        body: fdwav.body(),
        params: {
            headers: {
              'Content-Type': 'multipart/form-data; boundary=' + fdwav.boundary
            },
        },
};

export function resnet_func() {
  const res = http.post(resnet.url, resnet.body, resnet.params)
  check(res, {
    'is status 200': (r) => r.status === 200,
  });
}

export function rnnt_func() {
  const res = http.post(rnnt.url, rnnt.body, rnnt.params)
  check(res, {
    'is status 200': (r) => r.status === 200,
  });
}
