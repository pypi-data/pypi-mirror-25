# -*- coding: utf-8 -*-
"""
Elementary basis operations, Gram matrix and Gram-Schmidt orthogonalization.

..  moduleauthor:: Martin R.  Albrecht <martinralbrecht+fpylll@googlemail.com>

A ``MatGSO`` object stores the following information:

    - The integral basis `B`,

    - the Gram-Schmidt coefficients `μ_{i,j} = `⟨b_i, b^*_j⟩ / ||b^*_j||^2` for `i>j`, and

    - the coefficients `r_{i,j} = ⟨b_i, b^*_j⟩` for `i>j`

It holds that: `B = R × Q = (μ × D) × (D^{-1} × B^*)` where `Q` is orthonormal and `R` is lower
triangular.
"""

include "fpylll/config.pxi"

from cysignals.signals cimport sig_on, sig_off

from decl cimport gso_mpz_d, gso_mpz_ld, gso_mpz_dpe, gso_mpz_mpfr, fp_nr_t, zz_mat_core_t
from decl cimport gso_long_d, gso_long_ld, gso_long_dpe, gso_long_mpfr
from decl cimport d_t, ld_t
from fplll cimport FT_DOUBLE, FT_LONG_DOUBLE, FT_DPE, FT_MPFR, FloatType
from fplll cimport ZT_LONG, ZT_MPZ, IntType
from fplll cimport GSO_DEFAULT
from fplll cimport GSO_INT_GRAM
from fplll cimport GSO_OP_FORCE_LONG
from fplll cimport GSO_ROW_EXPO
from fplll cimport MatGSO as MatGSO_c, Z_NR, FP_NR, Matrix
from fplll cimport dpe_t
from fplll cimport get_current_slope
from fpylll.gmp.mpz cimport mpz_t
from fpylll.mpfr.mpfr cimport mpfr_t
from fpylll.util cimport preprocess_indices, check_float_type
from integer_matrix cimport IntegerMatrix

IF HAVE_QD:
    from decl cimport gso_mpz_dd, gso_mpz_qd, gso_long_dd, gso_long_qd, dd_t, qd_t
    from fplll cimport FT_DD, FT_QD

class MatGSORowOpContext(object):
    """
    A context in which performing row operations is safe.  When the context is left, the appropriate
    updates are performed by calling ``row_op_end()``.
    """
    def __init__(self, M, i, j):
        """Construct new context for ``M[i:j]``.

        :param M: MatGSO object
        :param i: start row
        :param j: stop row

        """
        self.i = i
        self.j = j
        self.M = M

    def __enter__(self):
        """
        Enter context for working on rows.

        """
        self.M.row_op_begin(self.i, self.j)
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """
        Exit context for working on rows.

        :param exception_type:
        :param exception_value:
        :param exception_traceback:

        """
        self.M.row_op_end(self.i, self.j)
        return False


cdef class MatGSO:
    """
    MatGSO provides an interface for performing elementary operations on a basis and computing its
    Gram matrix and its Gram-Schmidt orthogonalization.  The Gram-Schmidt coefficients are computed
    on demand.  The object keeps track of which coefficients are valid after each row operation.
    """

    def __init__(self, IntegerMatrix B, U=None, UinvT=None,
                 int flags=GSO_DEFAULT, float_type="double"):
        """
        :param IntegerMatrix B: The matrix on which row operations are performed.  It must not be
            empty.
        :param IntegerMatrix U: If ``U`` is not empty, operations on ``B`` are also done on ``u``
            (in this case both must have the same number of rows).  If ``u`` is initially the
            identity matrix, multiplying transform by the initial basis gives the current basis.
        :param IntegerMatrix UinvT: Inverse transform (should be empty, which disables the
            computation, or initialized with identity matrix).  It works only if ``U`` is not empty.
        :param int flags: Flags

                - ``GSO.INT_GRAM`` - If true, coefficients of the Gram matrix are computed with
                  exact integer arithmetic.  Otherwise, they are computed in floating-point.  Note
                  that when exact arithmetic is used, all coefficients of the first ``n_known_rows``
                  are continuously updated, whereas in floating-point, they are computed only
                  on-demand.  This option cannot be enabled when ``GSO.ROW_EXPO`` is set.

                - ``GSO.ROW_EXPO`` - If true, each row of ``B`` is normalized by a power of 2 before
                  doing conversion to floating-point, which hopefully avoids some overflows.  This
                  option cannot be enabled if ``GSO.INT_GRAM`` is set and works only with
                  ``float_type="double"`` and ``float_type="long double"``.  It is useless and
                  **must not** be used for ``float_type="dpe"``, ``float_type="dd"``,
                  ``float_type="qd"`` or ``float_type=mpfr_t``.

                - ``GSO.OP_FORCE_LONG`` - Affects the behaviour of ``row_addmul``.  See its
                  documentation.

        :param float_type: A floating point type, i.e. an element of ``fpylll.fpylll.float_types``.

        ..  note:: If ``float_type="mpfr"`` set precision with ``set_precision()`` before
            constructing this object and do not change the precision during the lifetime of this
            object.
        """

        if U is None:
            self.U = IntegerMatrix(0, 0)
        elif isinstance(U, IntegerMatrix):
            if U.nrows != B.nrows:
                raise ValueError("U.nrows != B.nrows")
            self.U = U

        if UinvT is None:
            self.UinvT = IntegerMatrix(0, 0)
        elif isinstance(UinvT, IntegerMatrix):
            if U is None:
                raise ValueError("Uinvt != None but U != None.")
            if UinvT.nrows != B.nrows:
                raise ValueError("UinvT.nrows != B.nrows")
            self.UinvT = UinvT

        cdef Matrix[Z_NR[mpz_t]] *b_m = <Matrix[Z_NR[mpz_t]]*>B._core.mpz
        cdef Matrix[Z_NR[mpz_t]] *u_m = <Matrix[Z_NR[mpz_t]]*>self.U._core.mpz
        cdef Matrix[Z_NR[mpz_t]] *u_inv_t_m = <Matrix[Z_NR[mpz_t]]*>self.UinvT._core.mpz
        cdef Matrix[Z_NR[long]] *b_l = <Matrix[Z_NR[long]]*>B._core.long
        cdef Matrix[Z_NR[long]] *u_l = <Matrix[Z_NR[long]]*>self.U._core.long
        cdef Matrix[Z_NR[long]] *u_inv_t_l = <Matrix[Z_NR[long]]*>self.UinvT._core.long

        cdef FloatType float_type_ = check_float_type(float_type)

        if B._type == ZT_MPZ:
            if float_type_ == FT_DOUBLE:
                self._type = gso_mpz_d
                self._core.mpz_d = new MatGSO_c[Z_NR[mpz_t],FP_NR[d_t]](b_m[0], u_m[0], u_inv_t_m[0], flags)
            elif float_type_ == FT_LONG_DOUBLE:
                IF HAVE_LONG_DOUBLE:
                    self._type = gso_mpz_ld
                    self._core.mpz_ld = new MatGSO_c[Z_NR[mpz_t],FP_NR[ld_t]](b_m[0], u_m[0], u_inv_t_m[0], flags)
                ELSE:
                    raise ValueError("Float type '%s' not understood." % float_type)
            elif float_type_ == FT_DPE:
                self._type = gso_mpz_dpe
                self._core.mpz_dpe = new MatGSO_c[Z_NR[mpz_t],FP_NR[dpe_t]](b_m[0], u_m[0], u_inv_t_m[0], flags)
            elif float_type_ == FT_MPFR:
                self._type = gso_mpz_mpfr
                self._core.mpz_mpfr = new MatGSO_c[Z_NR[mpz_t],FP_NR[mpfr_t]](b_m[0], u_m[0], u_inv_t_m[0], flags)
            else:
                IF HAVE_QD:
                    if float_type_ == FT_DD:
                        self._type = gso_mpz_dd
                        self._core.mpz_dd = new MatGSO_c[Z_NR[mpz_t],FP_NR[dd_t]](b_m[0], u_m[0], u_inv_t_m[0], flags)
                    elif float_type_ == FT_QD:
                        self._type = gso_mpz_qd
                        self._core.mpz_qd = new MatGSO_c[Z_NR[mpz_t],FP_NR[qd_t]](b_m[0], u_m[0], u_inv_t_m[0], flags)
                    else:
                        raise ValueError("Float type '%s' not understood."%float_type)
                ELSE:
                    raise ValueError("Float type '%s' not understood."%float_type)
        elif B._type == ZT_LONG:
            if float_type_ == FT_DOUBLE:
                self._type = gso_long_d
                self._core.long_d = new MatGSO_c[Z_NR[long],FP_NR[d_t]](b_l[0], u_l[0], u_inv_t_l[0], flags)
            elif float_type_ == FT_LONG_DOUBLE:
                IF HAVE_LONG_DOUBLE:
                    self._type = gso_long_ld
                    self._core.long_ld = new MatGSO_c[Z_NR[long],FP_NR[ld_t]](b_l[0], u_l[0], u_inv_t_l[0], flags)
                ELSE:
                    raise ValueError("Float type '%s' not understood." % float_type)
            elif float_type_ == FT_DPE:
                self._type = gso_long_dpe
                self._core.long_dpe = new MatGSO_c[Z_NR[long],FP_NR[dpe_t]](b_l[0], u_l[0], u_inv_t_l[0], flags)
            elif float_type_ == FT_MPFR:
                self._type = gso_long_mpfr
                self._core.long_mpfr = new MatGSO_c[Z_NR[long],FP_NR[mpfr_t]](b_l[0], u_l[0], u_inv_t_l[0], flags)
            else:
                IF HAVE_QD:
                    if float_type_ == FT_DD:
                        self._type = gso_long_dd
                        self._core.long_dd = new MatGSO_c[Z_NR[long],FP_NR[dd_t]](b_l[0], u_l[0], u_inv_t_l[0], flags)
                    elif float_type_ == FT_QD:
                        self._type = gso_long_qd
                        self._core.long_qd = new MatGSO_c[Z_NR[long],FP_NR[qd_t]](b_l[0], u_l[0], u_inv_t_l[0], flags)
                    else:
                        raise ValueError("Float type '%s' not understood."%float_type)
                ELSE:
                    raise ValueError("Float type '%s' not understood."%float_type)

        self.B = B

    def __dealloc__(self):
        if self._type == gso_long_d:
            del self._core.long_d
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                del self._core.long_ld
        if self._type == gso_long_dpe:
            del self._core.long_dpe
        IF HAVE_QD:
            if self._type == gso_long_dd:
                del self._core.long_dd
            if self._type == gso_long_qd:
                del self._core.long_qd
        if self._type == gso_long_mpfr:
            del self._core.long_mpfr

        if self._type == gso_mpz_d:
            del self._core.mpz_d
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                del self._core.mpz_ld
        if self._type == gso_mpz_dpe:
            del self._core.mpz_dpe
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                del self._core.mpz_dd
            if self._type == gso_mpz_qd:
                del self._core.mpz_qd
        if self._type == gso_mpz_mpfr:
            del self._core.mpz_mpfr

    def __reduce__(self):
        """
        Make sure attempts at pickling raise an error until proper pickling is implemented.
        """
        raise NotImplementedError

    @property
    def float_type(self):
        """
        >>> from fpylll import IntegerMatrix, GSO, set_precision
        >>> A = IntegerMatrix(10, 10)
        >>> M = GSO.Mat(A)
        >>> M.float_type
        'double'
        >>> set_precision(100)
        53
        >>> M = GSO.Mat(A, float_type='mpfr')
        >>> M.float_type
        'mpfr'

        """
        if self._type == gso_mpz_d or self._type == gso_long_d:
            return "double"
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld or self._type == gso_long_ld:
                return "long double"
        if self._type == gso_mpz_dpe or self._type == gso_long_dpe:
            return "dpe"
        IF HAVE_QD:
            if self._type == gso_mpz_dd or self._type == gso_long_dd:
                return "dd"
            if self._type == gso_mpz_qd or self._type == gso_long_qd:
                return "qd"
        if self._type == gso_mpz_mpfr or self._type == gso_long_mpfr:
            return "mpfr"

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    @property
    def int_type(self):
        """

        """
        if self._type in (gso_mpz_d, gso_mpz_dpe, gso_mpz_mpfr):
            return "mpz"
        elif self._type in (gso_long_d, gso_long_dpe, gso_long_mpfr):
            return "long"
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return "mpz"
            elif self._type == gso_long_ld:
                return "long"
        IF HAVE_QD:
            if self._type in (gso_mpz_dd, gso_mpz_qd):
                return "mpz"
            elif self._type in (gso_long_dd, gso_long_qd):
                return "long"

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    @property
    def d(self):
        """
        Number of rows of ``B`` (dimension of the lattice).

        >>> from fpylll import IntegerMatrix, GSO, set_precision
        >>> A = IntegerMatrix(11, 11)
        >>> M = GSO.Mat(A)
        >>> M.d
        11

        """
        if self._type == gso_mpz_d:
            return self._core.mpz_d.d
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.d
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.d
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.d
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.d
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.d

        if self._type == gso_long_d:
            return self._core.long_d.d
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.d
        if self._type == gso_long_dpe:
            return self._core.long_dpe.d
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.d
            if self._type == gso_long_qd:
                return self._core.long_qd.d
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.d

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    @property
    def int_gram_enabled(self):
        """
        Exact computation of dot products.

        >>> from fpylll import IntegerMatrix, GSO, set_precision
        >>> A = IntegerMatrix(11, 11)
        >>> M = GSO.Mat(A)
        >>> M.int_gram_enabled
        False

        >>> M = GSO.Mat(A, flags=GSO.INT_GRAM)
        >>> M.int_gram_enabled
        True

        """
        if self._type == gso_mpz_d:
            return bool(self._core.mpz_d.enable_int_gram)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return bool(self._core.mpz_ld.enable_int_gram)
        if self._type == gso_mpz_dpe:
            return bool(self._core.mpz_dpe.enable_int_gram)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return bool(self._core.mpz_dd.enable_int_gram)
            if self._type == gso_mpz_qd:
                return bool(self._core.mpz_qd.enable_int_gram)
        if self._type == gso_mpz_mpfr:
            return bool(self._core.mpz_mpfr.enable_int_gram)

        if self._type == gso_long_d:
            return bool(self._core.long_d.enable_int_gram)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return bool(self._core.long_ld.enable_int_gram)
        if self._type == gso_long_dpe:
            return bool(self._core.long_dpe.enable_int_gram)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return bool(self._core.long_dd.enable_int_gram)
            if self._type == gso_long_qd:
                return bool(self._core.long_qd.enable_int_gram)
        if self._type == gso_long_mpfr:
            return bool(self._core.long_mpfr.enable_int_gram)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    @property
    def row_expo_enabled(self):
        """
        Normalization of each row of b by a power of 2.

        >>> from fpylll import IntegerMatrix, GSO, set_precision
        >>> A = IntegerMatrix(11, 11)
        >>> M = GSO.Mat(A)
        >>> M.row_expo_enabled
        False

        >>> M = GSO.Mat(A, flags=GSO.ROW_EXPO)
        >>> M.row_expo_enabled
        True

        """
        if self._type == gso_mpz_d:
            return bool(self._core.mpz_d.enable_row_expo)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return bool(self._core.mpz_ld.enable_row_expo)
        if self._type == gso_mpz_dpe:
            return bool(self._core.mpz_dpe.enable_row_expo)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return bool(self._core.mpz_dd.enable_row_expo)
            if self._type == gso_mpz_qd:
                return bool(self._core.mpz_qd.enable_row_expo)
        if self._type == gso_mpz_mpfr:
            return bool(self._core.mpz_mpfr.enable_row_expo)

        if self._type == gso_long_d:
            return bool(self._core.long_d.enable_row_expo)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return bool(self._core.long_ld.enable_row_expo)
        if self._type == gso_long_dpe:
            return bool(self._core.long_dpe.enable_row_expo)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return bool(self._core.long_dd.enable_row_expo)
            if self._type == gso_long_qd:
                return bool(self._core.long_qd.enable_row_expo)
        if self._type == gso_long_mpfr:
            return bool(self._core.long_mpfr.enable_row_expo)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    @property
    def transform_enabled(self):
        """
        Computation of the transform matrix.

        >>> from fpylll import IntegerMatrix, GSO, set_precision
        >>> A = IntegerMatrix(11, 11)
        >>> M = GSO.Mat(A)
        >>> M.transform_enabled
        False

        >>> U = IntegerMatrix.identity(11)
        >>> M = GSO.Mat(A, U=U)

        >>> M.transform_enabled
        True

        """
        if self._type == gso_mpz_d:
            return bool(self._core.mpz_d.enable_transform)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return bool(self._core.mpz_ld.enable_transform)
        if self._type == gso_mpz_dpe:
            return bool(self._core.mpz_dpe.enable_transform)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return bool(self._core.mpz_dd.enable_transform)
            if self._type == gso_mpz_qd:
                return bool(self._core.mpz_qd.enable_transform)
        if self._type == gso_mpz_mpfr:
            return bool(self._core.mpz_mpfr.enable_transform)

        if self._type == gso_long_d:
            return bool(self._core.long_d.enable_transform)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return bool(self._core.long_ld.enable_transform)
        if self._type == gso_long_dpe:
            return bool(self._core.long_dpe.enable_transform)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return bool(self._core.long_dd.enable_transform)
            if self._type == gso_long_qd:
                return bool(self._core.long_qd.enable_transform)
        if self._type == gso_long_mpfr:
            return bool(self._core.long_mpfr.enable_transform)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    @property
    def inverse_transform_enabled(self):
        """
        Computation of the inverse transform matrix (transposed).

        >>> from fpylll import IntegerMatrix, GSO, set_precision
        >>> A = IntegerMatrix(11, 11)
        >>> M = GSO.Mat(A)
        >>> M.inverse_transform_enabled
        False

        >>> U = IntegerMatrix.identity(11)
        >>> UinvT = IntegerMatrix.identity(11)
        >>> M = GSO.Mat(A, U=U, UinvT=UinvT)
        >>> M.inverse_transform_enabled
        True

        """
        if self._type == gso_mpz_d:
            return bool(self._core.mpz_d.enable_inverse_transform)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return bool(self._core.mpz_ld.enable_inverse_transform)
        if self._type == gso_mpz_dpe:
            return bool(self._core.mpz_dpe.enable_inverse_transform)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return bool(self._core.mpz_dd.enable_inverse_transform)
            if self._type == gso_mpz_qd:
                return bool(self._core.mpz_qd.enable_inverse_transform)
        if self._type == gso_mpz_mpfr:
            return bool(self._core.mpz_mpfr.enable_inverse_transform)

        if self._type == gso_long_d:
            return bool(self._core.long_d.enable_inverse_transform)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return bool(self._core.long_ld.enable_inverse_transform)
        if self._type == gso_long_dpe:
            return bool(self._core.long_dpe.enable_inverse_transform)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return bool(self._core.long_dd.enable_inverse_transform)
            if self._type == gso_long_qd:
                return bool(self._core.long_qd.enable_inverse_transform)
        if self._type == gso_long_mpfr:
            return bool(self._core.long_mpfr.enable_inverse_transform)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    @property
    def row_op_force_long(self):
        """
        Changes the behaviour of ``row_addmul``, see its documentation.

        >>> from fpylll import IntegerMatrix, GSO, set_precision
        >>> A = IntegerMatrix(11, 11)
        >>> M = GSO.Mat(A)
        >>> M.row_op_force_long
        False

        >>> M = GSO.Mat(A, flags=GSO.OP_FORCE_LONG)
        >>> M.row_op_force_long
        True

        """
        if self._type == gso_mpz_d:
            return bool(self._core.mpz_d.row_op_force_long)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return bool(self._core.mpz_ld.row_op_force_long)
        if self._type == gso_mpz_dpe:
            return bool(self._core.mpz_dpe.row_op_force_long)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return bool(self._core.mpz_dd.row_op_force_long)
            if self._type == gso_mpz_qd:
                return bool(self._core.mpz_qd.row_op_force_long)
        if self._type == gso_mpz_mpfr:
            return bool(self._core.mpz_mpfr.row_op_force_long)

        if self._type == gso_long_d:
            return bool(self._core.long_d.row_op_force_long)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return bool(self._core.long_ld.row_op_force_long)
        if self._type == gso_long_dpe:
            return bool(self._core.long_dpe.row_op_force_long)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return bool(self._core.long_dd.row_op_force_long)
            if self._type == gso_long_qd:
                return bool(self._core.long_qd.row_op_force_long)
        if self._type == gso_long_mpfr:
            return bool(self._core.long_mpfr.row_op_force_long)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def row_op_begin(self, int first, int last):
        """
        Must be called before a sequence of ``row_addmul``.

        :param int first: start index for ``row_addmul`` operations.
        :param int last: final index (exclusive).

        .. note:: It is preferable to use ``MatGSORowOpContext`` via ``row_ops``.
        """
        if self._type == gso_mpz_d:
            return self._core.mpz_d.row_op_begin(first, last)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.row_op_begin(first, last)
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.row_op_begin(first, last)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.row_op_begin(first, last)
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.row_op_begin(first, last)
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.row_op_begin(first, last)

        if self._type == gso_long_d:
            return self._core.long_d.row_op_begin(first, last)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.row_op_begin(first, last)
        if self._type == gso_long_dpe:
            return self._core.long_dpe.row_op_begin(first, last)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.row_op_begin(first, last)
            if self._type == gso_long_qd:
                return self._core.long_qd.row_op_begin(first, last)
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.row_op_begin(first, last)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def row_op_end(self, int first, int last):
        """
        Must be called after a sequence of ``row_addmul``.  This invalidates the `i`-th line of the
        GSO.

        :param int first: start index to invalidate.
        :param int last:  final index to invalidate (exclusive).

        .. note:: It is preferable to use ``MatGSORowOpContext`` via ``row_ops``.
        """
        if self._type == gso_mpz_d:
            return self._core.mpz_d.row_op_end(first, last)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.row_op_end(first, last)
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.row_op_end(first, last)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.row_op_end(first, last)
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.row_op_end(first, last)
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.row_op_end(first, last)

        if self._type == gso_long_d:
            return self._core.long_d.row_op_end(first, last)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.row_op_end(first, last)
        if self._type == gso_long_dpe:
            return self._core.long_dpe.row_op_end(first, last)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.row_op_end(first, last)
            if self._type == gso_long_qd:
                return self._core.long_qd.row_op_end(first, last)
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.row_op_end(first, last)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def row_ops(self, int first, int last):
        """Return context in which ``row_addmul`` operations are safe.

        :param int first: start index.
        :param int last: final index (exclusive).

        """
        return MatGSORowOpContext(self, first, last)

    def get_gram(self, int i, int j):
        """
        Return Gram matrix coefficients (0 ≤ i ≤ ``n_known_rows`` and 0 ≤ j ≤ i).  If
        ``enable_row_expo`` is false, returns the dot product `⟨b_i, b_j⟩`.  If ``enable_row_expo``
        is true, returns `⟨b_i, b_j⟩/ 2^{(r_i + r_j)}`, where `r_i` and `r_j` are the row exponents
        of rows `i` and `j` respectively.

        :param int i:
        :param int j:

        """
        preprocess_indices(i, j, self.d, self.d)

        cdef fp_nr_t t

        # TODO: don't just return doubles
        if self._type == gso_mpz_d:
            return self._core.mpz_d.get_gram(t.d, i, j).get_d()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.get_gram(t.ld, i, j).get_d()
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.get_gram(t.dpe, i, j).get_d()
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.get_gram(t.dd, i, j).get_d()
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.get_gram(t.qd, i, j).get_d()
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.get_gram(t.mpfr, i, j).get_d()

        if self._type == gso_long_d:
            return self._core.long_d.get_gram(t.d, i, j).get_d()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.get_gram(t.ld, i, j).get_d()
        if self._type == gso_long_dpe:
            return self._core.long_dpe.get_gram(t.dpe, i, j).get_d()
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.get_gram(t.dd, i, j).get_d()
            if self._type == gso_long_qd:
                return self._core.long_qd.get_gram(t.qd, i, j).get_d()
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.get_gram(t.mpfr, i, j).get_d()

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def get_r(self, int i, int j):
        """
        Return `⟨b_i, b*_j⟩`.

        :param i:
        :param j:

        >>> from fpylll import *
        >>> A = IntegerMatrix.random(5, "uniform", bits=5)
        >>> M = GSO.Mat(A)
        >>> M.update_gso()
        True
        >>> M.get_r(1, 0)
        890.0

        """
        preprocess_indices(i, j, self.d, self.d)
        cdef fp_nr_t t

        # TODO: don't just return doubles
        if self._type == gso_mpz_d:
            return self._core.mpz_d.get_r(t.d, i, j).get_d()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.get_r(t.ld, i, j).get_d()
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.get_r(t.dpe, i, j).get_d()
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.get_r(t.dd, i, j).get_d()
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.get_r(t.qd, i, j).get_d()
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.get_r(t.mpfr, i, j).get_d()

        if self._type == gso_long_d:
            return self._core.long_d.get_r(t.d, i, j).get_d()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.get_r(t.ld, i, j).get_d()
        if self._type == gso_long_dpe:
            return self._core.long_dpe.get_r(t.dpe, i, j).get_d()
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.get_r(t.dd, i, j).get_d()
            if self._type == gso_long_qd:
                return self._core.long_qd.get_r(t.qd, i, j).get_d()
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.get_r(t.mpfr, i, j).get_d()

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def get_r_exp(self, int i, int j):
        """
        Return `f = r_{i, j}` and exponent `x` such that `⟨b_i, b^*_j⟩ = f ⋅ 2^x`.  If
        ``enable_row_expo`` is false, `x` is always 0.  If ``enable_row_expo`` is true, `x = r_i +
        r_j`, where `r_i` and `r_j` are the row exponents of rows `i` and `j` respectively.

        .. note:: It is assumed that `r(i, j)` is valid.

        :param i:
        :param j:

        """
        preprocess_indices(i, j, self.d, self.d)
        cdef double r = 0.0
        cdef long expo = 0

        # TODO: don't just return doubles
        if self._type == gso_mpz_d:
            r = self._core.mpz_d.get_r_exp(i, j, expo).get_data()
            return r, expo
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                r = self._core.mpz_ld.get_r_exp(i, j, expo).get_d()
                return r, expo
        if self._type == gso_mpz_dpe:
            r = self._core.mpz_dpe.get_r_exp(i, j, expo).get_d()
            return r, expo
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                r = self._core.mpz_dd.get_r_exp(i, j, expo).get_d()
                return r, expo
            if self._type == gso_mpz_qd:
                r = self._core.mpz_qd.get_r_exp(i, j, expo).get_d()
                return r, expo
        if self._type == gso_mpz_mpfr:
            r = self._core.mpz_mpfr.get_r_exp(i, j, expo).get_d()
            return r, expo

        if self._type == gso_long_d:
            r = self._core.long_d.get_r_exp(i, j, expo).get_data()
            return r, expo
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                r = self._core.long_ld.get_r_exp(i, j, expo).get_d()
                return r, expo
        if self._type == gso_long_dpe:
            r = self._core.long_dpe.get_r_exp(i, j, expo).get_d()
            return r, expo
        IF HAVE_QD:
            if self._type == gso_long_dd:
                r = self._core.long_dd.get_r_exp(i, j, expo).get_d()
                return r, expo
            if self._type == gso_long_qd:
                r = self._core.long_qd.get_r_exp(i, j, expo).get_d()
                return r, expo
        if self._type == gso_long_mpfr:
            r = self._core.long_mpfr.get_r_exp(i, j, expo).get_d()
            return r, expo

        raise RuntimeError("MatGSO object '%s' has no core."%self)


    def get_mu(self, int i, int j):
        """
        Return `<b_i, b^*_j> / ||b^*_j||^2`.

        :param i:
        :param j:

        """
        preprocess_indices(i, j, self.d, self.d)
        cdef fp_nr_t t

        # TODO: don't just return doubles
        if self._type == gso_mpz_d:
            return self._core.mpz_d.get_mu(t.d, i, j).get_d()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.get_mu(t.ld, i, j).get_d()
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.get_mu(t.dpe, i, j).get_d()
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.get_mu(t.dd, i, j).get_d()
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.get_mu(t.qd, i, j).get_d()
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.get_mu(t.mpfr, i, j).get_d()

        if self._type == gso_long_d:
            return self._core.long_d.get_mu(t.d, i, j).get_d()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.get_mu(t.ld, i, j).get_d()
        if self._type == gso_long_dpe:
            return self._core.long_dpe.get_mu(t.dpe, i, j).get_d()
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.get_mu(t.dd, i, j).get_d()
            if self._type == gso_long_qd:
                return self._core.long_qd.get_mu(t.qd, i, j).get_d()
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.get_mu(t.mpfr, i, j).get_d()

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def get_mu_exp(self, int i, int j):
        """
        Return `f = μ_{i, j}` and exponent `x` such that `f ⋅ 2^x = ⟨b_i, b^*_j⟩ / ‖b^*_j‖^2`.  If
        ``enable_row_expo`` is false, `x` is always zero.  If ``enable_row_expo`` is true, `x = r_i
        - r_j`, where `r_i` and `r_j` are the row exponents of rows `i` and `j` respectively.

        .. note:: It is assumed that `μ_{i, j}` is valid.

        :param i:
        :param j:

        """
        preprocess_indices(i, j, self.d, self.d)
        cdef double r = 0.0
        cdef long expo = 0

        # TODO: don't just return doubles
        if self._type == gso_mpz_d:
            r = self._core.mpz_d.get_mu_exp(i, j, expo).get_data()
            return r, expo
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                r = self._core.mpz_ld.get_mu_exp(i, j, expo).get_d()
                return r, expo
        if self._type == gso_mpz_dpe:
            r = self._core.mpz_dpe.get_mu_exp(i, j, expo).get_d()
            return r, expo
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                r = self._core.mpz_dd.get_mu_exp(i, j, expo).get_d()
                return r, expo
            if self._type == gso_mpz_qd:
                r = self._core.mpz_qd.get_mu_exp(i, j, expo).get_d()
                return r, expo
        if self._type == gso_mpz_mpfr:
            r = self._core.mpz_mpfr.get_mu_exp(i, j, expo).get_d()
            return r, expo

        if self._type == gso_long_d:
            r = self._core.long_d.get_mu_exp(i, j, expo).get_data()
            return r, expo
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                r = self._core.long_ld.get_mu_exp(i, j, expo).get_d()
                return r, expo
        if self._type == gso_long_dpe:
            r = self._core.long_dpe.get_mu_exp(i, j, expo).get_d()
            return r, expo
        IF HAVE_QD:
            if self._type == gso_long_dd:
                r = self._core.long_dd.get_mu_exp(i, j, expo).get_d()
                return r, expo
            if self._type == gso_long_qd:
                r = self._core.long_qd.get_mu_exp(i, j, expo).get_d()
                return r, expo
        if self._type == gso_long_mpfr:
            r = self._core.long_mpfr.get_mu_exp(i, j, expo).get_d()
            return r, expo

        raise RuntimeError("MatGSO object '%s' has no core."%self)


    def update_gso(self):
        """
        Updates all GSO coefficients (`μ` and `r`).
        """
        cdef int r
        if self._type == gso_mpz_d:
            with nogil:
                r = self._core.mpz_d.update_gso()
            return bool(r)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                with nogil:
                    r = self._core.mpz_ld.update_gso()
                return bool(r)
        if self._type == gso_mpz_dpe:
            with nogil:
                r = self._core.mpz_dpe.update_gso()
            return bool(r)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                with nogil:
                    r = self._core.mpz_dd.update_gso()
                return bool(r)
            if self._type == gso_mpz_qd:
                with nogil:
                    r = self._core.mpz_qd.update_gso()
                return bool(r)
        if self._type == gso_mpz_mpfr:
            with nogil:
                r = self._core.mpz_mpfr.update_gso()
            return bool(r)

        if self._type == gso_long_d:
            with nogil:
                r = self._core.long_d.update_gso()
            return bool(r)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                with nogil:
                    r = self._core.long_ld.update_gso()
                return bool(r)
        if self._type == gso_long_dpe:
            with nogil:
                r = self._core.long_dpe.update_gso()
            return bool(r)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                with nogil:
                    r = self._core.long_dd.update_gso()
                return bool(r)
            if self._type == gso_long_qd:
                with nogil:
                    r = self._core.long_qd.update_gso()
                return bool(r)
        if self._type == gso_long_mpfr:
            with nogil:
                r = self._core.long_mpfr.update_gso()
            return bool(r)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def update_gso_row(self, int i, int last_j):
        """
        Updates `r_{i, j}` and `μ_{i, j}` if needed for all `j` in `[0, last_j]`.  All coefficients
        of `r` and `μ` above the `i`-th row in columns `[0, min(last_j, i - 1)]` must be valid.

        :param int i:
        :param int last_j:

        """
        if self._type == gso_mpz_d:
            return bool(self._core.mpz_d.update_gso_row(i, last_j))
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return bool(self._core.mpz_ld.update_gso_row(i, last_j))
        if self._type == gso_mpz_dpe:
            return bool(self._core.mpz_dpe.update_gso_row(i, last_j))
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return bool(self._core.mpz_dd.update_gso_row(i, last_j))
            if self._type == gso_mpz_qd:
                return bool(self._core.mpz_qd.update_gso_row(i, last_j))
        if self._type == gso_mpz_mpfr:
            return bool(self._core.mpz_mpfr.update_gso_row(i, last_j))

        if self._type == gso_long_d:
            return bool(self._core.long_d.update_gso_row(i, last_j))
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return bool(self._core.long_ld.update_gso_row(i, last_j))
        if self._type == gso_long_dpe:
            return bool(self._core.long_dpe.update_gso_row(i, last_j))
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return bool(self._core.long_dd.update_gso_row(i, last_j))
            if self._type == gso_long_qd:
                return bool(self._core.long_qd.update_gso_row(i, last_j))
        if self._type == gso_long_mpfr:
            return bool(self._core.long_mpfr.update_gso_row(i, last_j))

        raise RuntimeError("MatGSO object '%s' has no core."%self)


    def discover_all_rows(self):
        """
        Allows ``row_addmul`` for all rows even if the GSO has never been computed.
        """
        if self._type == gso_mpz_d:
            return self._core.mpz_d.discover_all_rows()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.discover_all_rows()
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.discover_all_rows()
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.discover_all_rows()
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.discover_all_rows()
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.discover_all_rows()

        if self._type == gso_long_d:
            return self._core.long_d.discover_all_rows()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.discover_all_rows()
        if self._type == gso_long_dpe:
            return self._core.long_dpe.discover_all_rows()
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.discover_all_rows()
            if self._type == gso_long_qd:
                return self._core.long_qd.discover_all_rows()
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.discover_all_rows()

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def move_row(self, int old_r, int new_r):
        """
        Row ``old_r`` becomes row ``new_r`` and intermediate rows are shifted.
        If ``new_r < old_r``, then ``old_r`` must be ``< n_known_rows``.

        :param int old_r: row index
        :param int new_r: row index

        """
        preprocess_indices(old_r, new_r, self.d, self.d)
        if self._type == gso_mpz_d:
            return self._core.mpz_d.move_row(old_r, new_r)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.move_row(old_r, new_r)
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.move_row(old_r, new_r)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.move_row(old_r, new_r)
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.move_row(old_r, new_r)
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.move_row(old_r, new_r)

        if self._type == gso_long_d:
            return self._core.long_d.move_row(old_r, new_r)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.move_row(old_r, new_r)
        if self._type == gso_long_dpe:
            return self._core.long_dpe.move_row(old_r, new_r)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.move_row(old_r, new_r)
            if self._type == gso_long_qd:
                return self._core.long_qd.move_row(old_r, new_r)
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.move_row(old_r, new_r)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def swap_rows(self, int i, int j):
        """
        Swap rows ``i`` and ``j``.

        :param int i: row index
        :param int j: row index

        """
        preprocess_indices(i, j, self.d, self.d)
        if self._type == gso_mpz_d:
            return self._core.mpz_d.row_swap(i, j)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.row_swap(i, j)
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.row_swap(i, j)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.row_swap(i, j)
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.row_swap(i, j)
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.row_swap(i, j)

        if self._type == gso_long_d:
            return self._core.long_d.row_swap(i, j)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.row_swap(i, j)
        if self._type == gso_long_dpe:
            return self._core.long_dpe.row_swap(i, j)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.row_swap(i, j)
            if self._type == gso_long_qd:
                return self._core.long_qd.row_swap(i, j)
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.row_swap(i, j)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def negate_row(self, int i):
        """Set `b_i` to `-b_i`.

        :param int i: index of the row to negate

        Example::

            >>> from fpylll import *
            >>> set_random_seed(42)
            >>> A = IntegerMatrix(6, 6)
            >>> A.randomize("ntrulike", bits=6, q=31)
            >>> print(A)
            [ 1 0 0 12 25 25 ]
            [ 0 1 0 25 12 25 ]
            [ 0 0 1 25 25 12 ]
            [ 0 0 0 31  0  0 ]
            [ 0 0 0  0 31  0 ]
            [ 0 0 0  0  0 31 ]

            >>> M = GSO.Mat(A)
            >>> M.update_gso()
            True
            >>> with M.row_ops(2,2):
            ...     M.negate_row(2)
            ...
            >>> print(A)
            [ 1 0  0  12  25  25 ]
            [ 0 1  0  25  12  25 ]
            [ 0 0 -1 -25 -25 -12 ]
            [ 0 0  0  31   0   0 ]
            [ 0 0  0   0  31   0 ]
            [ 0 0  0   0   0  31 ]

        """
        self.row_addmul(i, i, -2.0)


    def row_addmul(self, int i, int j, x):
        """Set `b_i = b_i + x ⋅ b_j`.

        After one or several calls to ``row_addmul``, ``row_op_end`` must be called.

        If ``row_op_force_long=true``, ``x`` is always converted to (``2^expo * long``) instead of
        (``2^expo * ZT``), which is faster if ``ZT=mpz_t`` but might lead to a loss of precision in
        LLL, more Babai iterations are needed.

        :param int i: target row
        :param int j: source row
        :param x: multiplier

        """
        preprocess_indices(i, j, self.d, self.d)
        cdef fp_nr_t x_

        if self._type == gso_mpz_d:
            x_.d = float(x)
            return self._core.mpz_d.row_addmul(i, j, x_.d)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                x_.ld = float(x)
                return self._core.mpz_ld.row_addmul(i, j, x_.ld)
        if self._type == gso_mpz_dpe:
            x_.dpe = float(x)
            return self._core.mpz_dpe.row_addmul(i, j, x_.dpe)
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                x_.dd = float(x)
                return self._core.mpz_dd.row_addmul(i, j, x_.dd)
            if self._type == gso_mpz_qd:
                x_.qd = float(x)
                return self._core.mpz_qd.row_addmul(i, j, x_.qd)
        if self._type == gso_mpz_mpfr:
            x_.mpfr = float(x)
            return self._core.mpz_mpfr.row_addmul(i, j, x_.mpfr)

        if self._type == gso_long_d:
            x_.d = float(x)
            return self._core.long_d.row_addmul(i, j, x_.d)
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                x_.ld = float(x)
                return self._core.long_ld.row_addmul(i, j, x_.ld)
        if self._type == gso_long_dpe:
            x_.dpe = float(x)
            return self._core.long_dpe.row_addmul(i, j, x_.dpe)
        IF HAVE_QD:
            if self._type == gso_long_dd:
                x_.dd = float(x)
                return self._core.long_dd.row_addmul(i, j, x_.dd)
            if self._type == gso_long_qd:
                x_.qd = float(x)
                return self._core.long_qd.row_addmul(i, j, x_.qd)
        if self._type == gso_long_mpfr:
            x_.mpfr = float(x)
            return self._core.long_mpfr.row_addmul(i, j, x_.mpfr)

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def create_row(self):
        """Adds a zero row to ``B`` (and to ``U`` if ``enable_tranform=true``).  One or several
        operations can be performed on this row with ``row_addmul``, then ``row_op_end`` must be
        called.  Do not use if ``inverse_transform_enabled=true``.

        """
        if self.inverse_transform_enabled:
            raise ValueError("create_row is incompatible with ``inverse_transform_enabled``")

        if self._type == gso_mpz_d:
            return self._core.mpz_d.create_row()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.create_row()
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.create_row()
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.create_row()
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.create_row()
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.create_row()

        if self._type == gso_long_d:
            return self._core.long_d.create_row()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.create_row()
        if self._type == gso_long_dpe:
            return self._core.long_dpe.create_row()
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.create_row()
            if self._type == gso_long_qd:
                return self._core.long_qd.create_row()
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.create_row()

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def remove_last_row(self):
        """Remove.  the last row of ``B`` (and of ``U`` if ``enable_transform=true``).  Do not use
        if ``inverse_transform_enabled=true``.

        """
        if self.inverse_transform_enabled:
            raise ValueError("remove_last_row is incompatible with ``inverse_transform_enabled``")

        if self._type == gso_mpz_d:
            return self._core.mpz_d.remove_last_row()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                return self._core.mpz_ld.remove_last_row()
        if self._type == gso_mpz_dpe:
            return self._core.mpz_dpe.remove_last_row()
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                return self._core.mpz_dd.remove_last_row()
            if self._type == gso_mpz_qd:
                return self._core.mpz_qd.remove_last_row()
        if self._type == gso_mpz_mpfr:
            return self._core.mpz_mpfr.remove_last_row()

        if self._type == gso_long_d:
            return self._core.long_d.remove_last_row()
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                return self._core.long_ld.remove_last_row()
        if self._type == gso_long_dpe:
            return self._core.long_dpe.remove_last_row()
        IF HAVE_QD:
            if self._type == gso_long_dd:
                return self._core.long_dd.remove_last_row()
            if self._type == gso_long_qd:
                return self._core.long_qd.remove_last_row()
        if self._type == gso_long_mpfr:
            return self._core.long_mpfr.remove_last_row()

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def get_current_slope(self, int start_row, int stop_row):
        """
        Finds the slope of the curve fitted to the lengths of the vectors from ``start_row`` to
        ``stop_row``.  The slope gives an indication of the quality of the LLL-reduced basis.

        :param int start_row: start row index
        :param int stop_row: stop row index (exclusive)

        ..  note:: we call ``get_current_slope`` which is declared in bkz.h
        """

        preprocess_indices(start_row, stop_row, self.d, self.d+1)

        if self._type == gso_mpz_d:
            sig_on()
            r = self._core.mpz_d.get_current_slope(start_row, stop_row)
            sig_off()
            return r
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_mpz_ld:
                sig_on()
                r = self._core.mpz_ld.get_current_slope(start_row, stop_row)
                sig_off()
                return r
        if self._type == gso_mpz_dpe:
            sig_on()
            r = self._core.mpz_dpe.get_current_slope(start_row, stop_row)
            sig_off()
            return r
        IF HAVE_QD:
            if self._type == gso_mpz_dd:
                sig_on()
                r = self._core.mpz_dd.get_current_slope(start_row, stop_row)
                sig_off()
                return r
            if self._type == gso_mpz_qd:
                sig_on()
                r = self._core.mpz_qd.get_current_slope(start_row, stop_row)
                sig_off()
                return r
        if self._type == gso_mpz_mpfr:
            sig_on()
            r = self._core.mpz_mpfr.get_current_slope(start_row, stop_row)
            sig_off()
            return r

        if self._type == gso_long_d:
            sig_on()
            r = self._core.long_d.get_current_slope(start_row, stop_row)
            sig_off()
            return r
        IF HAVE_LONG_DOUBLE:
            if self._type == gso_long_ld:
                sig_on()
                r = self._core.long_ld.get_current_slope(start_row, stop_row)
                sig_off()
                return r
        if self._type == gso_long_dpe:
            sig_on()
            r = self._core.long_dpe.get_current_slope(start_row, stop_row)
            sig_off()
            return r
        IF HAVE_QD:
            if self._type == gso_long_dd:
                sig_on()
                r = self._core.long_dd.get_current_slope(start_row, stop_row)
                sig_off()
                return r
            if self._type == gso_long_qd:
                sig_on()
                r = self._core.long_qd.get_current_slope(start_row, stop_row)
                sig_off()
                return r
        if self._type == gso_long_mpfr:
            sig_on()
            r = self._core.long_mpfr.get_current_slope(start_row, stop_row)
            sig_off()
            return r

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def get_root_det(self, int start_row, int stop_row):
        """ Return (squared) root determinant of the basis.

        :param int start_row: start row (inclusive)
        :param int stop_row: stop row (exclusive)

        """
        preprocess_indices(start_row, stop_row, self.d, self.d+1)

        if self._type == gso_mpz_d:
            sig_on()
            r = self._core.mpz_d.get_root_det(start_row, stop_row).get_d()
            sig_off()
            return r
        elif self._type == gso_mpz_dpe:
            sig_on()
            r = self._core.mpz_dpe.get_root_det(start_row, stop_row).get_d()
            sig_off()
            return r
        elif self._type == gso_mpz_mpfr:
            sig_on()
            r = self._core.mpz_mpfr.get_root_det(start_row, stop_row).get_d()
            sig_off()
            return r
        else:
            IF HAVE_LONG_DOUBLE:
                if self._type == gso_mpz_ld:
                    sig_on()
                    r = self._core.mpz_ld.get_root_det(start_row, stop_row).get_d()
                    sig_off()
                    return r
            IF HAVE_QD:
                if self._type == gso_mpz_dd:
                    sig_on()
                    r = self._core.mpz_dd.get_root_det(start_row, stop_row).get_d()
                    sig_off()
                    return r
                elif self._type == gso_mpz_qd:
                    sig_on()
                    r = self._core.mpz_qd.get_root_det(start_row, stop_row).get_d()
                    sig_off()
                    return r

        if self._type == gso_long_d:
            sig_on()
            r = self._core.long_d.get_root_det(start_row, stop_row).get_d()
            sig_off()
            return r
        elif self._type == gso_long_dpe:
            sig_on()
            r = self._core.long_dpe.get_root_det(start_row, stop_row).get_d()
            sig_off()
            return r
        elif self._type == gso_long_mpfr:
            sig_on()
            r = self._core.long_mpfr.get_root_det(start_row, stop_row).get_d()
            sig_off()
            return r
        else:
            IF HAVE_LONG_DOUBLE:
                if self._type == gso_long_ld:
                    sig_on()
                    r = self._core.long_ld.get_root_det(start_row, stop_row).get_d()
                    sig_off()
                    return r
            IF HAVE_QD:
                if self._type == gso_long_dd:
                    sig_on()
                    r = self._core.long_dd.get_root_det(start_row, stop_row).get_d()
                    sig_off()
                    return r
                elif self._type == gso_long_qd:
                    sig_on()
                    r = self._core.long_qd.get_root_det(start_row, stop_row).get_d()
                    sig_off()
                    return r

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def get_log_det(self, int start_row, int stop_row):
        """ Return log of the (squared) determinant of the basis.

        :param int start_row: start row (inclusive)
        :param int stop_row: stop row (exclusive)

        """
        preprocess_indices(start_row, stop_row, self.d, self.d+1)

        if self._type == gso_mpz_d:
            sig_on()
            r = self._core.mpz_d.get_log_det(start_row, stop_row).get_d()
            sig_off()
            return r
        elif self._type == gso_mpz_dpe:
            sig_on()
            r = self._core.mpz_dpe.get_log_det(start_row, stop_row).get_d()
            sig_off()
            return r
        elif self._type == gso_mpz_mpfr:
            sig_on()
            r = self._core.mpz_mpfr.get_log_det(start_row, stop_row).get_d()
            sig_off()
            return r
        else:
            IF HAVE_LONG_DOUBLE:
                if self._type == gso_mpz_ld:
                    sig_on()
                    r = self._core.mpz_ld.get_log_det(start_row, stop_row).get_d()
                    sig_off()
                    return r
            IF HAVE_QD:
                if self._type == gso_mpz_dd:
                    sig_on()
                    r = self._core.mpz_dd.get_log_det(start_row, stop_row).get_d()
                    sig_off()
                    return r
                elif self._type == gso_mpz_qd:
                    sig_on()
                    r = self._core.mpz_qd.get_log_det(start_row, stop_row).get_d()
                    sig_off()
                    return r

        if self._type == gso_long_d:
            sig_on()
            r = self._core.long_d.get_log_det(start_row, stop_row).get_d()
            sig_off()
            return r
        elif self._type == gso_long_dpe:
            sig_on()
            r = self._core.long_dpe.get_log_det(start_row, stop_row).get_d()
            sig_off()
            return r
        elif self._type == gso_long_mpfr:
            sig_on()
            r = self._core.long_mpfr.get_log_det(start_row, stop_row).get_d()
            sig_off()
            return r
        else:
            IF HAVE_LONG_DOUBLE:
                if self._type == gso_long_ld:
                    sig_on()
                    r = self._core.long_ld.get_log_det(start_row, stop_row).get_d()
                    sig_off()
                    return r
            IF HAVE_QD:
                if self._type == gso_long_dd:
                    sig_on()
                    r = self._core.long_dd.get_log_det(start_row, stop_row).get_d()
                    sig_off()
                    return r
                elif self._type == gso_long_qd:
                    sig_on()
                    r = self._core.long_qd.get_log_det(start_row, stop_row).get_d()
                    sig_off()
                    return r

        raise RuntimeError("MatGSO object '%s' has no core."%self)

    def get_slide_potential(self, int start_row, int stop_row, int block_size):
        """ Return slide potential of the basis

        :param int start_row: start row (inclusive)
        :param int stop_row: stop row (exclusive)
        :param int block_size: block size

        """
        preprocess_indices(start_row, stop_row, self.d, self.d+1)

        if self._type == gso_mpz_d:
            sig_on()
            r = self._core.mpz_d.get_slide_potential(start_row, stop_row, block_size).get_d()
            sig_off()
            return r
        elif self._type == gso_mpz_dpe:
            sig_on()
            r = self._core.mpz_dpe.get_slide_potential(start_row, stop_row, block_size).get_d()
            sig_off()
            return r
        elif self._type == gso_mpz_mpfr:
            sig_on()
            r = self._core.mpz_mpfr.get_slide_potential(start_row, stop_row, block_size).get_d()
            sig_off()
            return r
        else:
            IF HAVE_LONG_DOUBLE:
                if self._type == gso_mpz_ld:
                    sig_on()
                    r = self._core.mpz_ld.get_slide_potential(start_row, stop_row, block_size).get_d()
                    sig_off()
                    return r
            IF HAVE_QD:
                if self._type == gso_mpz_dd:
                    sig_on()
                    r = self._core.mpz_dd.get_slide_potential(start_row, stop_row, block_size).get_d()
                    sig_off()
                    return r
                elif self._type == gso_mpz_qd:
                    sig_on()
                    r = self._core.mpz_qd.get_slide_potential(start_row, stop_row, block_size).get_d()
                    sig_off()
                    return r

        if self._type == gso_long_d:
            sig_on()
            r = self._core.long_d.get_slide_potential(start_row, stop_row, block_size).get_d()
            sig_off()
            return r
        elif self._type == gso_long_dpe:
            sig_on()
            r = self._core.long_dpe.get_slide_potential(start_row, stop_row, block_size).get_d()
            sig_off()
            return r
        elif self._type == gso_long_mpfr:
            sig_on()
            r = self._core.long_mpfr.get_slide_potential(start_row, stop_row, block_size).get_d()
            sig_off()
            return r
        else:
            IF HAVE_LONG_DOUBLE:
                if self._type == gso_long_ld:
                    sig_on()
                    r = self._core.long_ld.get_slide_potential(start_row, stop_row, block_size).get_d()
                    sig_off()
                    return r
            IF HAVE_QD:
                if self._type == gso_long_dd:
                    sig_on()
                    r = self._core.long_dd.get_slide_potential(start_row, stop_row, block_size).get_d()
                    sig_off()
                    return r
                elif self._type == gso_long_qd:
                    sig_on()
                    r = self._core.long_qd.get_slide_potential(start_row, stop_row, block_size).get_d()
                    sig_off()
                    return r

        raise RuntimeError("MatGSO object '%s' has no core."%self)


    def from_canonical(self, v, int start=0, int dimension=-1):
        """Given a vector `v` wrt the canonical basis `\mathbb{Z}^n` return a vector wrt the
        Gram-Schmidt basis `B^*`

        :param v: a tuple-like object of dimension ``M.B.ncols``
        :param start: only consider subbasis starting at ``start```
        :param dimension: only consider ``dimension`` vectors or all if ``-1``

        :returns: a tuple of dimension ``dimension``` or ``M.d``` when ``dimension`` is ``None``

        This operation is the inverse of ``to_canonical``::

            >>> import random
            >>> A = IntegerMatrix.random(5, "uniform", bits=6)
            >>> M = GSO.Mat(A)
            >>> _ = M.update_gso()
            >>> v = tuple(IntegerMatrix.random(5, "uniform", bits=6)[0]); v
            (35, 24, 55, 40, 23)
            >>> w = M.from_canonical(v); w # doctest: +ELLIPSIS
            (0.98294..., 0.5636..., -3.4594479..., 0.9768..., 0.261316...)
            >>> v_ = tuple([int(round(wi)) for wi in M.to_canonical(w)]); v_
            (35, 24, 55, 40, 23)
            >>> v == v_
            True

        """
        cdef Py_ssize_t i, j, d

        if dimension == -1:
            d = self.d - start
        else:
            d = dimension

        cdef list ret = [0]*(start+d)
        for i in range(start+d):
            for j in range(self.B.ncols):
                ret[i] += self.B[i, j] * v[j]

            for j in range(i):
                ret[i] -= self.get_mu(i, j) * ret[j]

        # we drop the first ``start`` entries anyway, so no need to update
        for i in range(d):
            ret[start+i] /= self.get_r(start+i, start+i)

        return tuple(ret)[start:]


    def to_canonical(self, v, int start=0):
        """
        Given a vector `v` wrt the Gram-Schmidt basis `B^*` return a vector wrt the canonical basis
        `\mathbb{Z}^n`

        :param v: a tuple-like object of dimension ``M.d``
        :param start: only consider subbasis starting at ``start```

        :returns: a tuple of dimension ``M.B.ncols``

        """

        cdef list vv = list(v)
        cdef Py_ssize_t i, j
        cdef Py_ssize_t d = min(len(vv), self.d-start)
        for i in range(d)[::-1]:
            for j in range(i+1, d):
                vv[i] -= self.get_mu(start+j, start+i) * vv[j]

        ret = [0]*self.B.ncols
        for i in range(d):
            for j in range(self.B.ncols):
                ret[j] += vv[i] * self.B[start+i,j]

        return tuple(ret)


    def babai(self, v, int start=0, int dimension=-1, gso=False):
        """
        Return lattice vector close to `v` using Babai's nearest plane algorithm.

        :param v: a tuple-like object
        :param start: only consider subbasis starting at ``start```
        :param dimension: only consider ``dimension`` vectors or all if ``-1```
        :param gso: if ``True`` vector is represented wrt to the Gram-Schmidt basis, otherwise
            canonical basis is assumed.

        :returns: a tuple of dimension `M.B.nrows`
        """
        if dimension == -1:
            dimension = self.d - start
        if not gso:
            v = self.from_canonical(v, start, dimension)

        cdef Py_ssize_t i, j
        cdef list vv = list(v)
        for i in range(dimension)[::-1]:
            vv[i] = int(round(vv[i]))
            for j in range(i):
                vv[j] -= self.get_mu(start+i, start+j) * vv[i]
        return tuple(vv)

    def r(self, start=0, end=-1):
        """
        Return ``r`` vector from ``start`` to ``end``
        """
        if end == -1:
            end = self.d
        return tuple([self.get_r(i, i) for i in range(start, end)])

class GSO:
    DEFAULT=GSO_DEFAULT
    INT_GRAM=GSO_INT_GRAM
    ROW_EXPO=GSO_ROW_EXPO
    OP_FORCE_LONG=GSO_OP_FORCE_LONG
    Mat = MatGSO
