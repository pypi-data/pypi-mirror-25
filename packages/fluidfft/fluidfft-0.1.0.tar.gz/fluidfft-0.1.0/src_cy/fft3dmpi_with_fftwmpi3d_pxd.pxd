
cdef extern from "base_fft.h":
    ctypedef struct mycomplex:
        pass

cdef extern from "fft3dmpi_with_fftwmpi3d.h":
    cdef cppclass FFT3DMPIWithFFTWMPI3D:
        int test()
        const char* bench(int)

        int get_local_size_X()
        int get_local_size_K()

        void get_local_shape_X(int*, int*, int*)
        void get_local_shape_K(int*, int*, int*)

        void get_global_shape_X(int*, int*, int*)
        void get_global_shape_K(int*, int*, int*)

        void get_dimX_K(int*, int*, int*)
        void get_seq_indices_first_K(int*, int*)
        
        FFT3DMPIWithFFTWMPI3D(int, int, int) except +

        void destroy()

        const char* get_classname()

        void fft(double* fieldX, mycomplex* fieldK)
        void ifft(mycomplex* fieldK, double* fieldX)

        double sum_wavenumbers_double(double* fieldK)
        void sum_wavenumbers_complex(mycomplex* fieldK, mycomplex* result)
        
        double compute_energy_from_X(double* fieldX)
        double compute_energy_from_K(mycomplex* fieldK)
        double compute_mean_from_X(double* fieldX)
        double compute_mean_from_K(mycomplex* fieldK)
