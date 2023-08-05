from gmp.mpz cimport mpz_t
from fplll.fplll cimport FloatType, Z_NR, PrunerMetric, IntType
from fplll.fplll cimport BKZParam as BKZParam_c
from fpylll.fplll.fplll cimport PrunerMetric

cdef FloatType check_float_type(object float_type)
cdef IntType check_int_type(object int_type)
cdef int preprocess_indices(int &i, int &j, int m, int n) except -1
cdef int check_precision(int precision) except -1
cdef int check_eta(float eta) except -1
cdef int check_delta(float delta) except -1
cdef PrunerMetric check_pruner_metric(object metric)
