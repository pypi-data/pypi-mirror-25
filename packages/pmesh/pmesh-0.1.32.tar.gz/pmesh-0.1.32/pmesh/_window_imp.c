#define UNLIKELY(x) (x)
#define LIKELY(x) (x)

#include <stddef.h>
#include <stdint.h>
#include <math.h>
#include "_window_imp.h"

#include "_window_wavelets.h"
#include "_window_lanczos.h"

static void
_fill_k(PMeshPainter * painter, double pos[], int ipos[], double * k)
{
    double gpos[painter->ndim];
    int d;

    for(d = 0; d < painter->ndim; d++) {
        double * kd = &k[painter->support * d];

        gpos[d] = pos[d] * painter->scale[d] + painter->translate[d];
        ipos[d] = floor(gpos[d] + painter->shift) - painter->left;
        double dx = gpos[d] - ipos[d]; /* relative to the left most nonzero.*/
        int i;
        for(i = 0; i < painter->support; i ++) {
            double x = (dx - i) * painter->vfactor;
            if(painter->order[d] == 0) {
                kd[i] = painter->kernel(x) * painter->vfactor;
            } else {
                kd[i] = painter->diff(x) * painter->scale[d] * painter->vfactor * painter->vfactor;
            }
        }
        /* Watch out: do not renormalize per particle */

        /* We require the kernels to be properly normalized instead,
         * because the sampling here is too coarse for individual renormalizing to make sense.
         * -- the normalization is very different for different offsets.
         */

        /*
         * the total mass of individual point is not supposed to conserve when we resample an
         * image. Nevertheless when we add them all up the total is statistically conserved.
         */
    }
}

#define FLOAT float
#define mkname(a) a ## _ ## float
#include "_window_generics.h"
#include "_window_tuned_nnb.h"
#include "_window_tuned_cic.h"
#include "_window_tuned_tsc.h"
#undef FLOAT
#undef mkname
#undef ACCESS3
#undef ACCESS2
#define mkname(a) a ## _ ## double
#define FLOAT double
#include "_window_generics.h"
#include "_window_tuned_nnb.h"
#include "_window_tuned_cic.h"
#include "_window_tuned_tsc.h"
#undef FLOAT
#undef mkname
#undef ACCESS3
#undef ACCESS2

static double
_nearest_kernel(double x) {
    /* implementiong nearest in floating is poor due to round-off errors */
    if(x < 0.5 && x >= - 0.5)
        return 1.0;
    return 0;
}

static double
_nearest_diff(double x) {
    return 0;
}


static double
_linear_kernel(double x) {
    x = fabs(x);
    if(x < 1.0)
        return 1.0 - x;
    return 0;
}

static double
_linear_diff(double x) {
    double factor;
    if(x < 0) {
        factor = 1;
        x = - x;
    } else if (x > 0) {
        factor = - 1;
    } else {
        factor = 0;
    }
    if(x < 1.0) return factor;
    return 0;
}

static double
_quadratic_kernel(double x) {
    /*
     * Take from https://arxiv.org/abs/0804.0070
     * */
    x = fabs(x);
    if(x <= 0.5) {
        return 0.75 - x * x;
    }
    if(x < 1.5) {
        x = 1.5 - x;
        return (x * x) * 0.5;
    }
    return 0;
}

static double
_quadratic_diff(double x) {
    double factor;
    if ( x < 0) {
        x = -x;
        factor = -1;
    } else {
        factor = +1;
    }

    if(x <= 0.5) {
        return factor * (- 2 * x);
    }
    if(x < 1.5) {
        return factor * (- (1.5 - x));
    }
    return 0;
}

static double
_cubic_kernel(double x) {
    const double alpha = -0.5;
    /*
     * alpha = -0.5 is good. taken from
     * http://www.ipol.im/pub/art/2011/g_lmii/revisions/2011-09-27/g_lmii.html
     * */
    x = fabs(x);
    double xx = x * x;
    if(x < 1.0) {
        return (alpha + 2) * xx * x - (alpha + 3) * xx + 1;
    }
    if (x < 2) {
        return (alpha * xx * x) - 5 * alpha * xx + 8 * alpha * x - 4 * alpha;
    }
    return 0;
}

static double
_cubic_diff(double x) {
    const double alpha = -0.5;
    /*
     * alpha = -0.5 is good. taken from
     * http://www.ipol.im/pub/art/2011/g_lmii/revisions/2011-09-27/g_lmii.html
     * */
    double factor;
    if (x < 0) {
        factor = -1;
        x = -x;
    } else {
        factor = +1;
    }

    double xx = x * x;
    if(x < 1.0) {
        return factor * (3 * (alpha + 2) * xx - 2 * (alpha + 3) * x);
    }
    if(x < 2.0) {
        return factor * (3 * (alpha * xx) - 10 * alpha * x + 8 * alpha);
    }
    return 0;
}

static int
_compatible_with_nnb_tuned(PMeshPainter * painter, int ndim)
{
    if(painter->type != PMESH_PAINTER_TUNED_NNB) return 0;
    if(painter->ndim != ndim) return 0;
    if(painter->order[0] > 1) return 0;
    if(ndim > 1 && painter->order[1] > 1) return 0;
    if(ndim > 2 && painter->order[2] > 1) return 0;
    if(painter->support != 1 && painter->support > 0) return 0;
    return 1;
}


static int
_compatible_with_cic_tuned(PMeshPainter * painter, int ndim)
{
    if(painter->type != PMESH_PAINTER_TUNED_CIC) return 0;
    if(painter->ndim != ndim) return 0;
    if(painter->order[0] > 1) return 0;
    if(ndim > 1 && painter->order[1] > 1) return 0;
    if(ndim > 2 && painter->order[2] > 1) return 0;
    if(painter->support != 2 && painter->support > 0) return 0;
    return 1;
}

static int
_compatible_with_tsc_tuned(PMeshPainter * painter, int ndim)
{
    if(painter->type != PMESH_PAINTER_TUNED_TSC) return 0;
    if(painter->ndim != ndim) return 0;
    if(painter->order[0] > 1) return 0;
    if(ndim > 1 && painter->order[1] > 1) return 0;
    if(ndim > 2 && painter->order[2] > 1) return 0;
    if(painter->support != 3 && painter->support > 0) return 0;
    return 1;
}

void
pmesh_painter_init(PMeshPainter * painter)
{
    if(painter->canvas_dtype_elsize == 8) {
        painter->paint = _generic_paint_double;
        painter->readout = _generic_readout_double;
    } else {
        painter->paint = _generic_paint_float;
        painter->readout = _generic_readout_float;
    }

    switch(painter->type) {
        case PMESH_PAINTER_NEAREST:
            painter->kernel = _nearest_kernel;
            painter->diff = _nearest_diff;
            painter->nativesupport = 1;
        break;
        case PMESH_PAINTER_LINEAR:
            painter->kernel = _linear_kernel;
            painter->diff = _linear_diff;
            painter->nativesupport = 2;
        break;
        case PMESH_PAINTER_QUADRATIC:
            painter->kernel = _quadratic_kernel;
            painter->diff = _quadratic_diff;
            painter->nativesupport = 3;
        break;
        case PMESH_PAINTER_CUBIC:
            painter->kernel = _cubic_kernel;
            painter->diff = _cubic_diff;
            painter->nativesupport = 4;
        break;
        case PMESH_PAINTER_LANCZOS2:
            painter->kernel = _lanczos2_kernel;
            painter->diff = _lanczos2_diff;
            painter->nativesupport = _lanczos2_nativesupport;
        break;
        case PMESH_PAINTER_LANCZOS3:
            painter->kernel = _lanczos3_kernel;
            painter->diff = _lanczos3_diff;
            painter->nativesupport = _lanczos3_nativesupport;
        break;
        case PMESH_PAINTER_LANCZOS4:
            painter->kernel = _lanczos4_kernel;
            painter->diff = _lanczos4_diff;
            painter->nativesupport = _lanczos4_nativesupport;
        break;
        case PMESH_PAINTER_LANCZOS5:
            painter->kernel = _lanczos5_kernel;
            painter->diff = _lanczos5_diff;
            painter->nativesupport = _lanczos5_nativesupport;
        break;
        case PMESH_PAINTER_LANCZOS6:
            painter->kernel = _lanczos6_kernel;
            painter->diff = _lanczos6_diff;
            painter->nativesupport = _lanczos6_nativesupport;
        break;
        case PMESH_PAINTER_DB6:
            painter->kernel = _db6_kernel;
            painter->diff = _db6_diff;
            painter->nativesupport = _db6_nativesupport;
        break;
        case PMESH_PAINTER_DB12:
            painter->kernel = _db12_kernel;
            painter->diff = _db12_diff;
            painter->nativesupport = _db12_nativesupport;
        break;
        case PMESH_PAINTER_DB20:
            painter->kernel = _db20_kernel;
            painter->diff = _db20_diff;
            painter->nativesupport = _db20_nativesupport;
        break;
        case PMESH_PAINTER_SYM6:
            painter->kernel = _sym6_kernel;
            painter->diff = _sym6_diff;
            painter->nativesupport = _sym6_nativesupport;
        break;
        case PMESH_PAINTER_SYM12:
            painter->kernel = _sym12_kernel;
            painter->diff = _sym12_diff;
            painter->nativesupport = _sym12_nativesupport;
        break;
        case PMESH_PAINTER_SYM20:
            painter->kernel = _sym20_kernel;
            painter->diff = _sym20_diff;
            painter->nativesupport = _sym20_nativesupport;
        break;
#define CASE_TUNED(xxx_tuned) \
            if(_compatible_with_ ## xxx_tuned (painter, 2)) { \
                if(painter->canvas_dtype_elsize == 8) { \
                    painter->paint = _ ## xxx_tuned ## _paint2_double; \
                    painter->readout = _ ## xxx_tuned ## _readout2_double; \
                } else { \
                    painter->paint = _ ## xxx_tuned ## _paint2_float; \
                    painter->readout = _ ## xxx_tuned ## _readout2_float; \
                } \
                break; \
            } \
            if(_compatible_with_ ## xxx_tuned (painter, 3)) { \
                if(painter->canvas_dtype_elsize == 8) { \
                    painter->paint = _ ## xxx_tuned ## _paint3_double; \
                    painter->readout = _ ## xxx_tuned ## _readout3_double; \
                } else { \
                    painter->paint = _ ## xxx_tuned ## _paint3_float; \
                    painter->readout = _ ## xxx_tuned ## _readout3_float; \
                } \
                break; \
            }
        case PMESH_PAINTER_TUNED_NNB:
            /* fall back to use nearest kernel */
            painter->kernel = _nearest_kernel;
            painter->diff = _nearest_diff;
            painter->nativesupport = 1;
            CASE_TUNED(nnb_tuned)
        break;
        case PMESH_PAINTER_TUNED_CIC:
            /* fall back to use linear kernel */
            painter->kernel = _linear_kernel;
            painter->diff = _linear_diff;
            painter->nativesupport = 2;
            CASE_TUNED(cic_tuned)
        break;
        case PMESH_PAINTER_TUNED_TSC:
            /* fall back to use quad kernel */
            painter->kernel = _quadratic_kernel;
            painter->diff = _quadratic_diff;
            painter->nativesupport = 3;
            CASE_TUNED(tsc_tuned)
        break;
#undef CASE_TUNED
    }

    if(painter->support <= 0) {
        painter->support = painter->nativesupport;
    }

    painter->left = (painter->support - 1) / 2;
    if (painter->support % 2 == 0){
        painter->shift = 0;
    } else {
        painter->shift = 0.5;
    }
    int nmax = 1;
    int d;
    for(d = 0; d < painter->ndim; d++) {
        nmax *= (painter->support);
    }
    painter->Npoints = nmax;
    painter->vfactor = painter->nativesupport / (1. * painter->support);
}

void
pmesh_painter_paint(PMeshPainter * painter, double pos[], double weight)
{
    painter->paint(painter, pos, weight);
}

double
pmesh_painter_readout(PMeshPainter * painter, double pos[])
{
    return painter->readout(painter, pos);
}

