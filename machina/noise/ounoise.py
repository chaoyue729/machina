# Copyright 2018 DeepX Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from machina.noise.base import BaseActionNoise
import numpy as np
import torch
from machina.utils import get_device

class OUActionNoise(BaseActionNoise):
    def __init__(self, ac_space, sigma=0.2, theta=.15, dt=1e-2, x0=None):
        BaseActionNoise.__init__(self, ac_space)
        self.mu = np.zeros(self.ac_space[0])
        self.theta = theta
        self.sigma = sigma * np.ones_like(self.mu)
        self.dt = dt
        self.x0 = x0
        self.reset()

    def __call__(self):
        x = self.x_prev + self.theta * (self.mu - self.x_prev) * self.dt + self.sigma * np.sqrt(self.dt) * np.random.normal(size=self.mu.shape)
        self.x_prev = x
        return torch.tensor(x, dtype=torch.float, device=get_device())

    def reset(self):
        if self.x0 is not None:
            self.x_prev = self.x0
        else:
            self.x_prev = np.zeros_like(self.mu, dtype=np.float32)