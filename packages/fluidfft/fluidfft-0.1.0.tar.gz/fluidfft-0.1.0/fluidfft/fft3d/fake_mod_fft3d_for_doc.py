
class FFT3dFakeForDoc(object):
    """Perform fast Fourier transform in 3D.

    """
    def __init__(self, n0=2, n1=2, n2=4):
        pass

    def get_local_size_X(self):
        pass

    def run_tests(self):
        pass

    def run_benchs(self, nb_time_execute=10):
        pass

    def fft_as_arg(self, fieldX, fieldK):
        pass

    def ifft_as_arg(self, fieldK, fieldX):
        pass

    def fft(self, fieldX):
        pass

    def ifft(self, fieldK):
        pass

    def get_shapeX_loc(self):
        """Get the shape of the array in real space for this mpi process."""

    def get_shapeK_loc(self):
        """Get the shape of the array in Fourier space for this mpi process."""

    def get_shapeX_seq(self):
        """Get the shape of an array in real space for a sequential run."""

    def gather_Xspace(self, ff_loc, root=None):
        """Gather an array in real space for a parallel run."""

    def scatter_Xspace(self, ff_seq, root=None):
        """Scatter an array in real space for a parallel run."""

    def get_shapeK_seq(self):
        """Get the shape of an array in Fourier space for a sequential run."""

    def sum_wavenumbers(self, fieldK):
        """Compute the sum over all wavenumbers."""

    def get_dimX_K(self):
        """Get the indices of the real space dimension in Fourier space."""

    def get_seq_indices_first_K(self):
        """Get the "sequential" index of the first number in Fourier space."""

    def get_k_adim_loc(self):
        """Get the non-dimensional wavenumbers stored locally.

        returns k0_adim_loc, k1_adim_loc, k2_adim_loc.

        """

    def build_invariant_arrayX_from_2d_indices12X(self, o2d, arr2d):
        pass

    def build_invariant_arrayK_from_2d_indices12X(self, o2d, arr2d):
        pass
