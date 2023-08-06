# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Cython wrapper for ``surface.f90``."""


cdef extern from "bezier/surface.h":
    void de_casteljau_one_round(
        int *num_nodes, int *dimension, double *nodes, int *degree,
        double *lambda1, double *lambda2, double *lambda3, double *new_nodes)
    void evaluate_barycentric(
        int *num_nodes, int *dimension, double *nodes, int *degree,
        double *lambda1, double *lambda2, double *lambda3, double *point)
    void evaluate_barycentric_multi(
        int *num_nodes, int *dimension, double *nodes, int *degree,
        int *num_vals, double *param_vals, double *evaluated)
    void evaluate_cartesian_multi(
        int *num_nodes, int *dimension, double *nodes, int *degree,
        int *num_vals, double *param_vals, double *evaluated)
    void jacobian_both(
        int *num_nodes, int *dimension, double *nodes,
        int *degree, double *new_nodes)
    void jacobian_det(
        int *num_nodes, double *nodes, int *degree,
        int *num_vals, double *param_vals, double *evaluated)
