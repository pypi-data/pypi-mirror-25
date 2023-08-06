#*****************************************************************************
#    AUTHOR:  Han Frederic <frederic.han@imj-prg.fr>
#  2012
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
"""
giacpy: Interface to the C++ library giac (Computer Algebra System).


Giac is a general computer algebra system created by Bernard Parisse. It is used in Xcas.

Homepage http://www-fourier.ujf-grenoble.fr/~parisse/giac.html


The natural way to use giacpy is through the giac function. This function creates a Pygen object and evaluate it with the giac C++ library.

The initialisation of a Pygen just create an object in the C++ library giac, but the mathematical computation  is not done. This class is mainly usefull for cython users.


EXAMPLES::

    >>> from giacpy import giac
    >>> x,y,z=giac('x,y,z');  # define some basic giac objects
    >>> f=(x+3*y)/(x+z+1)**2 -(x+z+1)**2/(x+3*y)  # then we can compute
    >>> f.factor()
    (3*y-x**2-2*x*z-x-z**2-2*z-1)*(3*y+x**2+2*x*z+3*x+z**2+2*z+1)/((x+z+1)**2*(3*y+x))
    >>> f.normal()
    (-x**4-4*x**3*z-4*x**3-6*x**2*z**2-12*x**2*z-5*x**2+6*x*y-4*x*z**3-12*x*z**2-12*x*z-4*x+9*y**2-z**4-4*z**3-6*z**2-4*z-1)/(x**3+3*x**2*y+2*x**2*z+2*x**2+6*x*y*z+6*x*y+x*z**2+2*x*z+x+3*y*z**2+6*y*z+3*y)

. To obtain more hints on giacpy consider the help of the giac function.

    >>> help(giac)             # doctest: +SKIP

GETTING HELP::

#. To obtain some help on a giac keyword use the help() method. To open the more detailled (local) html documentation in an external browser, use:  htmlhelp()

    >>> from giacpy import *
    >>> gcd.help()              # doctest: +SKIP
    "Returns the greatest common divisor of 2 polynomials of several variables or of 2 integers or of 2 rationals.
    (Intg or Poly),(Intg or Poly)
    gcd(45,75);gcd(15/7,50/9);gcd(x^2-2*x+1,x^3-1);gcd(t^2-2*t+1,t^2+t-2);gcd((x^2-1)*(y^2-1)*z^2,x^3*y^3*z+(-(y^3))*z+x^3*z-z)
    lcm,euler,modgcd,ezgcd,psrgcd,heugcd,Gcd"
    >>> gcd.htmlhelp('fr')          # doctest: +SKIP

#. You can find full html documentation in several languages (en, fr, el) at:

   http://www-fourier.ujf-grenoble.fr/~parisse/giac/doc/en/cascmd_en/

   or you can try to open its local copy with the command:

    >>> from giacpy import htmlhelp
    >>> htmlhelp()        # doctest: +SKIP
    >>> htmlhelp('fr')    # doctest: +SKIP

#. You can import more giac/xcas keywords to work in a symbolic ring.

EXAMPLES::

    >>> from giacpy import *
    >>> x=giac('x');f=1/(2+sin(5*x))
    >>> f.int()
    2/5/sqrt(3)*(atan((-sqrt(3)*sin(5*x)+cos(5*x)+2*sin(5*x)+1)/(sqrt(3)*cos(5*x)+sqrt(3)-2*cos(5*x)+sin(5*x)+2))+5*x/2)
    >>> f.series(x,0,3)
    1/2-5/4*x+25/8*x**2-125/48*x**3+x**4*order_size(x)
    >>> (sqrt(5)+pi).approx(100)
    5.377660631089582934871817052010779119637787758986631545245841837718337331924013898042449233720899343

#. Cas Settings. Some convenient settings are obtained from: giacsettings:

    >>> from giacpy import giacsettings


#. Graphics 2D Output. If your version of giacpy has built giacpy2qcas, you can send graphics to qcas. For experimental interactive geometry see: help(qcas)

EXAMPLES::

    >>> from giacpy import *
    >>> C=giac('plot(x*sin(x)),x=-3*pi,3*pi')
    >>> C.qcas()             # doctest: +SKIP
    >>> l=[(C*t*0.1).color(t) for t in range(10)]
    >>> giac(l).qcas)        # doctest: +SKIP
    >>> A=randvector(200)
    >>> (histogram(classes(A,0,10))).qcas()         # doctest: +SKIP
    >>> C=giac('plot(sin(x)/x),x=-3*pi,3*pi')
    >>> C.qcas()             # doctest: +SKIP
    >>> l=[(C*t*0.1).color(t) for t in range(10)]
    >>> giac(l).qcas()       # doctest: +SKIP


"""
########################################################

cimport giacpy

from webbrowser import open as wwwbrowseropen
from sys import maxsize as Pymaxint
import os
import math

from time import sleep
from cpython.exc cimport PyErr_CheckSignals

#### Python3 compatibility  #############################
from sys import version_info as Pyversioninfo
if Pyversioninfo[0]>2 :
   PythonVersion3 = True
else:
   PythonVersion3 = False

def decstring23(s):
  if PythonVersion3 :
      return s.decode()
  else:
      return s


def encstring23(s):
  if PythonVersion3 :
      return bytes(s,'UTF-8')
  else:
      return s


if PythonVersion3:
    listrange=list,range
else:
    listrange=list

####End of Python3 compatibility########################

########################################################
#   Don't forget to include the    CTRL C settings     #
#   for giac, otherwise CTRL C might kill the session  #

include 'interrupt.pxi'
########################################################


########################################################
# A global context pointer. One by giac session.
########################################################
context_ptr=new context()
#
# Some global variables for optimisation
GIACNULL=Pygen('NULL')
#



# Create a giac setting instance
giacsettings=GiacSetting()


# remove lock to enable write access from giac
unsetsecure_run()


#######################################################
# The wrapper to eval with giac
#######################################################
def giac(s):
  """
    This function evaluate a python object with the giac library.

    * It creates in python a Pygen element and evaluate it with giac. For instance\
 to compute a trigonometric expansion of cos(x+2y) where x and y are just formal\
 symbols  we can do:

     >>> from giacpy import giac,pi
     >>> x,y=giac('x,y')
     >>> (x+2*y).cos().texpand()
     cos(x)*(2*cos(y)**2-1)-sin(x)*2*cos(y)*sin(y)


   Coercion, Pygen and internal giac variables:
   --------------------------------------------

   * The most usefull objects will be the Python object of type Pygen. In the following\
 example, we start by defining symbols x,y,z and do some formal computations

    >>> from giacpy import *
    >>> x,y,z=giac('x,y,z')
    >>> ((x+2*y/z)*(y+1)**2).diff(y)  # compute the partial derivative with respect to y
    2/z*(y+1)**2+(x+2*y/z)*2*(y+1)

    In the next example x was previously defined as a symbol so x[i] is just another symbol.\
 So we can use the symbols x[i] to work with polynomial in several variables as we do with the\
other symbols x,y,z.

    For instance to compute the coefficient of x[0]^12 in (x[0]+x[1]+x[2]+x[3]+x[4])^15/(y+z)\
 we just do the following
    >>> f=sum([x[i] for i in range(5)])**15/(y+z);f.coeff(x[0],12)
    (455*(x[1])**3+1365*(x[1])**2*x[2]+1365*(x[1])**2*x[3]+1365*(x[1])**2*x[4]+1365*x[1]*(x[2])**2+2730*x[1]*x[2]*x[3]+2730*x[1]*x[2]*x[4]+1365*x[1]*(x[3])**2+2730*x[1]*x[3]*x[4]+1365*x[1]*(x[4])**2+455*(x[2])**3+1365*(x[2])**2*x[3]+1365*(x[2])**2*x[4]+1365*x[2]*(x[3])**2+2730*x[2]*x[3]*x[4]+1365*x[2]*(x[4])**2+455*(x[3])**3+1365*(x[3])**2*x[4]+1365*x[3]*(x[4])**2+455*(x[4])**3)/(y+z)

      Warning: The complex number sqrt(-1) is exported in python as I. (But it may appears as i)

    >>> ((1+I*sqrt(3))**3).normal(); 1+I
    -8
    1+i

   * Python integers and reals can be directly converted to giac.

    >>> a=giac(2**1024);a.nextprime();(giac(1.234567)).erf().approx(10)
    179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137859
    0.9191788641


   * There are some natural coercion to Pygen elements:

    >>> pi>3.14 ; pi >3.15 ; giac(3)==3
    True
    False
    True

   But sometimes you need to prevent Python from doing a computation before the conversion. For example\
 if 1/3 is done in Python2 you will obtain 0 while in Python3 0.33333 so to create: x+1/3:
   >>> x+'1/3'
   x+1/3
   >>> x+giac(1)/3
   x+1/3

   while to create x/(1+x) or x+x/3 you don't need quotes because at each step one of the two object is a Pygen.
   >>> x/(1+x)
   x/(1+x)
   >>> (x+x/3).factor()
   4*x/3


   * The Python object y defined above is of type Pygen. It is not an internal giac variable. (Most of the time you won't need to use internal giac variables).

    >>> yyyy=2;giac('yyyy:=1');yyyy
    1
    2


   Linear Algebra:
   ---------------

   * In Giac/Xcas vectors are just lists and matrices are lists of list.

    >>> x,y=giac('x,y')
    >>> A=giac([[1,2],[3,4]])  # we create a giac matrix from it lines
    >>> v=giac([x,y]); v   # a giac vector
    [x,y]
    >>> A*v # matrix product with a vector outputs a vector
    [x+2*y,3*x+4*y]
    >>> v*v  # dot product
    x*x+y*y

    Remark that w=giac([[x],[y]]) is a matrix of 1 column and 2 rows. It is not a vector\
    so w*w doesn't make sense.
    >>> w=giac([[x],[y]])
    >>> w.transpose()*w   # this matrix product makes sense and output a 1x1 matrix.
    matrix[[x*x+y*y]]

   * In Python affectation doesn't create a new matrix. (cf. pointers) see also \
 the doc of  'giacpy.Pygen.__setitem__'

    >>> B1=A;
    >>> B1[0,0]=43; B1 # in place affectation changes both B1 and A
    [[43,2],[3,4]]
    >>> A
    [[43,2],[3,4]]
    >>> A[0][0]=A[0][0]+1; A  # similar as A[0,0]=A[0,0]+1
    [[44,2],[3,4]]
    >>> A.pcar(x)  # compute the characteristic polynomial of A
    x**2-48*x+170
    >>> B2=A.copy() # use copy to create another object
    >>> B2[0,0]=55; B2  # here A is not modified
    [[55,2],[3,4]]
    >>> A
    [[44,2],[3,4]]



   * Sparse Matrices are avaible via the table function.
    >>> import giacpy
    >>> A=giacpy.table(()); A  # create an empty giac table
    table(
    )
    >>> A[2,3]=33; A[0,2]='2/7' # set non zero entries of the sparse matrix
    >>> A*A  # basic matrix operation are supported with sparse matrices
    table(
    (0,3) = 66/7
    )
    >>> D=giacpy.diag([22,3,'1/7']); D  # some diagonal matrix
    [[22,0,0],[0,3,0],[0,0,1/7]]
    >>> giacpy.table(D)    # to create a sparse matrix from an ordinary one
    table(
    (0,0) = 22,
    (1,1) = 3,
    (2,2) = 1/7
    )


     But many matrix functions apply only with ordinary matrices so need conversions

    >>> B1=A.matrix(); B1 # convert the sparse matrix to a matrix, but the size is minimal
    [[0,0,2/7,0],[0,0,0,0],[0,0,0,33]]
    >>> B2=B1.redim(4,4); B2.pmin(x)  # so we may need to resize B1
    x**3


   Lists of Pygen and Giac lists:
   ------------------------------

   * Here l1 is a giac list and l2 is a python list of Pygen type objects.

    >>> l1=giac(range(10)); l2=[1/(i**2+1) for i in l1]
    >>> sum(l2)
    33054527/16762850

    So l1+l1 is done in giac and means a vector addition. But l2+l2 is done in Python so it is the list concatenation.

    >>> l1+l1
    [0,2,4,6,8,10,12,14,16,18]

    >>> l2+l2
    [1, 1/2, 1/5, 1/10, 1/17, 1/26, 1/37, 1/50, 1/65, 1/82, 1, 1/2, 1/5, 1/10, 1/17, 1/26, 1/37, 1/50, 1/65, 1/82]


   * Here V is not a Pygen element. We need to push it to giac to use a giac method like dim, or we need to use an imported function.

    >>> V=[ [x[i]**j for i in range(8)] for j in range(8)]

    >>> giac(V).dim()
    [8,8]

    >>> det_minor(V).factor()
    (x[6]-(x[7]))*(x[5]-(x[7]))*(x[5]-(x[6]))*(x[4]-(x[7]))*(x[4]-(x[6]))*(x[4]-(x[5]))*(x[3]-(x[7]))*(x[3]-(x[6]))*(x[3]-(x[5]))*(x[3]-(x[4]))*(x[2]-(x[7]))*(x[2]-(x[6]))*(x[2]-(x[5]))*(x[2]-(x[4]))*(x[2]-(x[3]))*(x[1]-(x[7]))*(x[1]-(x[6]))*(x[1]-(x[5]))*(x[1]-(x[4]))*(x[1]-(x[3]))*(x[1]-(x[2]))*(x[0]-(x[7]))*(x[0]-(x[6]))*(x[0]-(x[5]))*(x[0]-(x[4]))*(x[0]-(x[3]))*(x[0]-(x[2]))*(x[0]-(x[1]))


   * Modular objects with %

    >>> V=ranm(5,6) % 2;

    >>> ker(V).rowdim()+V.rank()
    6

    >>> a=giac(7)%3;a;a%0;7%3
    1 % 3
    1
    1

   Do not confuse with the  python integers:

    >>> type(7%3)==type(a);type(a)==type(7%3)
    False
    False

   Syntaxes with reserved or unknown Python symbols:
   -------------------------------------------------

   * In general equations needs symbols such as = < > or that have another meaning in Python. So those objects must be quoted.

 ::

    >>> from giacpy import *

    >>> x=giac('x')

    >>> (1+2*sin(3*x)).solve(x).simplify()
    list[-pi/18,7*pi/18]

    >>> solve('sin(3*x)>2*sin(x)',x)
    "Unable to find numeric values solving equation. For trigonometric equations this may be solved using assumptions, e.g. assume(x>-pi && x<pi) Error: Bad Argument Value"


   * You can also add some hypothesis to a giac symbol:

    >>> assume('x>-pi && x<pi')
    x
    >>> solve('sin(3*x)>2*sin(x)',x)
    list[((x>(-5*pi/6)) and (x<(-pi/6))),((x>0) and (x<(pi/6))),((x>(5*pi/6)) and (x<pi))]

   * To remove those hypothesis use the giac function: purge

    >>> purge('x')
    assume[[],[line[-pi,pi]],[-pi,pi]]
    >>> solve('x>0')
    list[x>0]

 ::

   * Same problems with the ..

    >>> from giacpy import *

    >>> x=giac('x')

    >>> f=1/(5+cos(4*x));f.int(x)
    1/2/(2*sqrt(6))*(atan((-sqrt(6)*sin(4*x)+2*sin(4*x))/(sqrt(6)*cos(4*x)+sqrt(6)-2*cos(4*x)+2))+4*x/2)
    >>> fMax(f,'x=-0..pi').simplify()
    pi/4,3*pi/4
    >>> fMax.help()    # doctest: +SKIP
    "Returns the abscissa of the maximum of the expression.
    Expr,[Var]
    fMax(-x^2+2*x+1,x)
    fMin"
    >>> sum(1/(1+x**2),'x=0..infinity').simplify()
    (pi*exp(pi)**2+pi+exp(pi)**2-1)/(2*exp(pi)**2-2)


   MEMENTO of usual GIAC functions:
   ===============================

   * Expand with simplification

         - ``ratnormal``, ``normal``, ``simplify``   (from the fastest to the most sophisticated)

         -  NB: ``expand`` function doesn't regroup nor cancel terms, so it could be slow. (pedagogical purpose only?)

   * Factor/Regroup

         - ``factor``, ``factors``, ``regroup``, ``cfactor``, ``ifactor``

   * Misc

         - ``unapply``, ``op``, ``subst``

   * Polynomials/Fractions

         - ``coeff``,  ``gbasis``, ``greduce``, ``lcoeff``, ``pcoeff``, ``canonical_form``,

         - ``proot``,  ``poly2symb``,  ``symb2poly``, ``posubLMQ``, ``poslbdLMQ``, ``VAS``, ``tcoeff``,  ``valuation``

         - ``gcd``, ``egcd``, ``lcm``, ``quo``, ``rem``, ``quorem``, ``abcuv``, ``chinrem``,

         - ``peval``, ``horner``, ``lagrange``, ``ptayl``, ``spline``,  ``sturm``,  ``sturmab``

         - ``partfrac``, ``cpartfrac``

   * Memory/Variables

         * ``assume``, ``about``, ``purge``, ``ans``

   * Calculus/Exact

         - ``linsolve``,  ``solve``,  ``csolve``,  ``desolve``,  ``seqsolve``, ``reverse_rsolve``, ``matpow``

         - ``limit``, ``series``, ``sum``, ``diff``, ``fMax``, ``fMin``,

         - ``integrate``, ``subst``, ``ibpdv``, ``ibpu``, ``preval``

   * Calculus/Exp, Log, powers

         - ``exp2pow``, ``hyp2exp``, ``expexpand``, ``lin``, ``lncollect``, ``lnexpand``, ``powexpand``, ``pow2exp``

   * Trigo

         - ``trigexpand``, ``tsimplify``, ``tlin``, ``tcollect``,

         - ``halftan``, ``cos2sintan``, ``sin2costan``, ``tan2sincos``, ``tan2cossin2``, ``tan2sincos2``, ``trigcos``, ``trigsin``, ``trigtan``, ``shift_phase``

         - ``exp2trig``, ``trig2exp``

         - ``atrig2ln``, ``acos2asin``, ``acos2atan``, ``asin2acos``, ``asin2atan``, ``atan2acos``, ``atan2asin``

   * Linear Algebra

         - ``identity``, ``matrix``, ``makemat``, ``syst2mat``, ``matpow``, ``table``,  ``redim``

         - ``det``,  ``det_minor``, ``rank``, ``ker``, ``image``, ``rref``, ``simplex_reduce``,

         - ``egv``, ``egvl``,  ``eigenvalues``, ``pcar``, ``pcar_hessenberg``, ``pmin``,

         - ``jordan``, ``adjoint_matrix``, ``companion``, ``hessenberg``, ``transpose``,

         - ``cholesky``, ``lll``,  ``lu``, ``qr``, ``svd``, ``a2q``, ``gauss``, ``gramschmidt``,
           ``q2a``, ``isom``, ``mkisom``


   * Finite Fieds

         - ``%``, ``% 0``, ``mod``, ``GF``, ``powmod``


   * Integers

         - ``gcd``, ``iabcuv``, ``ichinrem``, ``idivis``, ``iegcd``,

         - ``ifactor``, ``ifactors``, ``iquo``, ``iquorem``, ``irem``,

         - ``is_prime, is_pseudoprime``, ``lcm``, ``mod``, ``nextprime``, ``pa2b2``, ``prevprime``,
           ``smod``, ``euler``, ``fracmod``

   * List

         - ``append``, ``accumulate_head_tail``, ``concat``, ``head``, ``makelist``, ``member``, ``mid``, ``revlist``, ``rotate``, ``shift``, ``size``, ``sizes``, ``sort``, ``suppress``, ``tail``

   * Set

         - ``intersect``, ``minus``, ``union``, ``is_element``, ``is_included``


  """
  return Pygen(s).threadeval()


#######################################
# A class to adjust giac configuration
#######################################
cdef class GiacSetting(Pygen):
     """
     A class to customise the Computer Algebra  System settings

     * property threads:

         Maximal number of allowed theads in giac

     * property digits:

         Default digits number used for approximations:

         ::

             >>> from giacpy import giacsettings,giac
             >>> giacsettings.digits=20;giacsettings.digits
             20
             >>> giac('1/7').approx()
             0.14285714285714285714
             >>> giacsettings.digits=12;

     * property sqrtflag:

         Flag to allow sqrt extractions during solve and factorizations:

         ::

             >>> from giacpy import giac,giacsettings
             >>> giacsettings.sqrtflag=False;giacsettings.sqrtflag
             False
             >>> giac('x**2-2').factor()
             x**2-2
             >>> giacsettings.sqrtflag=True;
             >>> giac('x**2-2').factor()
             (x-sqrt(2))*(x+sqrt(2))

     * property complexflag:

         Flag to allow complex number in solving equations or factorizations:

         ::

            >>> from giacpy import giac,giacsettings
            >>> giacsettings.complexflag=False;giacsettings.complexflag
            False
            >>> giac('x**2+4').factor()
            x**2+4
            >>> giacsettings.complexflag=True;
            >>> giac('x**2+4').factor()
            (x+2*i)*(x-2*i)


     * property eval_level:

         Recursive level of substitution of variables during an evaluation:

         ::

             >>> from giacpy import giacsettings,giac
             >>> giacsettings.eval_level=1
             >>> giac("purge(a):;b:=a;a:=1;b")
             "Done",a,1,a
             >>> giacsettings.eval_level=25; giacsettings.eval_level
             25
             >>> giac("purge(a):;b:=a;a:=1;b")
             "Done",a,1,1

     * property proba_epsilon:

         Maximum probability of a wrong answer with a probabilist algorithm.
         Set this number to 0 to disable probabilist algorithms (slower):

         ::

             >>> from giacpy import giacsettings,giac
             >>> giacsettings.proba_epsilon=0;giac('proba_epsilon')
             0.0
             >>> giacsettings.proba_epsilon=10^(-13)
             >>> giac('proba_epsilon')<10^(-14)
             False

     * property epsilon:

         Value used by the epsilon2zero function:

         ::

             >>> from giacpy import giacsettings,giac
             >>> giacsettings.epsilon=1e-10
             >>> x=giac('x')
             >>> P=giac('1e-11+x+5')
             >>> P==x+5
             False
             >>> (P.epsilon2zero()).simplify()
             x+5

     """

     def __repr__(self):
       return "Giac Settings"


     property digits:
         r"""
         Default digits number used for approximations:

         ::

            >>> from giacpy import giac,giacsettings
            >>> giacsettings.digits=20;giacsettings.digits
            20
            >>> giac('1/7').approx()
            0.14285714285714285714
            >>> giacsettings.digits=12;

         """
         def __get__(self):
           return (self.cas_setup()[6])._val


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           pl[6]=value
           Pygen('cas_setup(%s)'%(pl)).eval()


     property sqrtflag:
         r"""
         Flag to allow square roots in solving equations or factorizations:

         ::

            >>> from giacpy import giac,giacsettings
            >>> giacsettings.sqrtflag=False;giacsettings.sqrtflag
            False
            >>> giac('x**2-2').factor()
            x**2-2
            >>> giacsettings.sqrtflag=True;
            >>> giac('x**2-2').factor()
            (x-sqrt(2))*(x+sqrt(2))

         """
         def __get__(self):
           return (self.cas_setup()[9])._val == 1


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           if value:
              pl[9]=1
           else:
              pl[9]=0
           Pygen('cas_setup(%s)'%(pl)).eval()


     property complexflag:
         r"""
         Flag to allow complex number in solving equations or factorizations:

         ::

            >>> from giacpy import giac,giacsettings
            >>> giacsettings.complexflag=False;giacsettings.complexflag
            False
            >>> giac('x**2+4').factor()
            x**2+4
            >>> giacsettings.complexflag=True;
            >>> giac('x**2+4').factor()
            (x+2*i)*(x-2*i)

         """
         def __get__(self):
           return (self.cas_setup()[2])._val == 1


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           if value:
              pl[2]=1
           else:
              pl[2]=0
           Pygen('cas_setup(%s)'%(pl)).eval()


     property eval_level:
         """
         Recursive level of substitution of variables during an evaluation:

            >>> from giacpy import giacsettings,purge
            >>> giacsettings.eval_level=1
            >>> giac("purge(a):;b:=a;a:=1;b")
            "Done",a,1,a
            >>> giacsettings.eval_level=25; giacsettings.eval_level
            25
            >>> giac("purge(a):;b:=a;a:=1;b")
            "Done",a,1,1

         """
         def __get__(self):
           return (self.cas_setup()[7][3])._val


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           pl[7]=[l[7][0],l[7][1],l[7][2],value]
           Pygen('cas_setup(%s)'%(pl)).eval()



     property proba_epsilon:
         """
         Maximum probability of a wrong answer with a probabilist algorithm.
         Set this number to 0 to disable probabilist algorithms (slower):

            >>> from giacpy import giacsettings,giac
            >>> giacsettings.proba_epsilon=0;giac('proba_epsilon')
            0.0
            >>> giacsettings.proba_epsilon=10**(-15);giac('proba_epsilon')=='1e-15'
            True

         """
         def __get__(self):
           return (self.cas_setup()[5][1])._double


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           pl[5]=[l[5][0],value]
           Pygen('cas_setup(%s)'%(pl)).eval()


     property epsilon:
         r"""
         Value used by the epsilon2zero function:

         ::

            >>> from giacpy import giac,giacsettings
            >>> giacsettings.epsilon=1e-10
            >>> P=giac('1e-11+x+5')
            >>> P==x+5
            False
            >>> (P.epsilon2zero()).simplify()
            x+5

         """
         def __get__(self):
           return (self.cas_setup()[5][0])._double


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           pl[5]=[value,l[5][1]]
           Pygen('cas_setup(%s)'%(pl)).eval()

     property threads:
         """
         Maximal number of allowed theads in giac
         """
         def __get__(self):
           return (self.cas_setup()[7][0])._val

         def __set__(self,value):
           Pygen('threads:=%s'%(str(value))).eval()



########################################################
#                                                      #
#    The python class that points to a cpp giac gen    #
#                                                      #
########################################################
cdef class Pygen:


     def __cinit__(self, s=None):

         #NB: the  != here gives problems with  the __richcmp__ function
         #if (s!=None):
         # so it's better to use isinstance
         if (isinstance(s,None.__class__)):
             # Do NOT replace with: self=GIACNULL  (cf the doctest in __repr__
             self.gptr = new gen ((<Pygen>GIACNULL).gptr[0])
             return

         if isinstance(s,int):       # This looks 100 faster than the str initialisation
           if PythonVersion3:
             #in python3 int and long are int
             if s.bit_length()< Pymaxint.bit_length():
                self.gptr = new gen(<long long>s)
             else:
                self.gptr = new gen(pylongtogen(s))
           else:
                self.gptr = new gen(<long long>s)

         #
         # Warning: the conversion to double is faster than strings but some Digits look lost?
         # not so much as it first look : giac(1/7.0)._double -1/7.0

         elif isinstance(s,float):
             self.gptr = new gen(<double>s)
         #

         elif isinstance(s,long):
             #s=str(s)
             #self.gptr = new gen(<string>s,context_ptr)
             self.gptr = new gen(pylongtogen(s))


         elif isinstance(s,Pygen):
             #in the test: x,y=Pygen('x,y');((x+2*y).sin()).texpand()
             # the y are lost without this case.
             self.gptr = new gen((<Pygen>s).gptr[0])


         elif isinstance(s,listrange):
             self.gptr = new gen(_wrap_pylist(<list>s),<short int>0)

         elif isinstance(s,tuple):
             self.gptr = new gen(_wrap_pylist(<tuple>s),<short int>1)

         # Other types are converted with strings.
         else:
           if not(isinstance(s,str)):  #modif python3
             s=s.__str__()
             #s=s.__repr__()   # with big gen repr is intercepted
           #self.gptr = new gen(<string>s,context_ptr)
           self.gptr = new gen(<string>encstring23(s),context_ptr)


     def __dealloc__(self):
         del self.gptr


     def __repr__(self):
        """
         >>> vide=Pygen()
         >>> vide
         NULL

        """
        #if self.gptr == NULL:
        #  return ''
        try:
          # fast evaluation of the complexity of the gen. (it's not the number of char )
          t=GIAC_taille(self.gptr[0], 6000)
        except:
          raise RuntimeError
        if (t<6000) :
           return decstring23(GIAC_print(self.gptr[0], context_ptr).c_str()) #python3
        else:
          return str(self.type)+"\nResult is too big for Display. If you really want to see it use print"

     def __str__(self):
        #if self.gptr == NULL:
        #  return ''
        return decstring23(GIAC_print(self.gptr[0], context_ptr).c_str()) #python3

     def __len__(self):
       #if (self.gptr != NULL):
         try:
           rep=GIAC_size(self.gptr[0],context_ptr).val
           #GIAC_size return a gen. we take the int: val
           return rep
         except:
           raise RuntimeError
       #else:
       #  raise MemoryError,"This Pygen is not associated to a giac gen"


     def __getitem__(self,i):  #TODO?: add gen support for indexes
        """
         Lists of 10**6 integers should be translated to giac easily

           >>> l=giac(list(range(10**6)));l[5]   #python3
           5
           >>> l[35:50:7]
           [35,42,49]
           >>> t=giac(tuple(range(10)))
           >>> t[:4:-1]
           9,8,7,6,5
           >>> x=giac('x'); sum([ x[i] for i in range(5)])**3
           (x[0]+x[1]+x[2]+x[3]+x[4])**3
           >>> import giacpy
           >>> A=giacpy.ranm(5,10); A[3,7]-A[3][7]
           0
           >>> A.transpose()[8,2]-A[2][8]
           0
           >>> A=giac('[ranm(5,5),ranm(5,5)]')
           >>> A[1,2,3]-A[1][2][3]
           0

        Crash test:

           >>> l=Pygen()
           >>> l[0]
           Traceback (most recent call last):
             File "<stdin>", line 1, in <module>
           ...
           IndexError: list index 0 out of range

        """
        cdef gen result

        if(self._type == 7) or (self._type == 12):   #if self is a list or a string
          if isinstance(i,int):
            n=len(self)
            if(i<n)and(-i<n):
                if(i<0):
                  i=i+n
                try:
                  result=self.gptr[0][<int>i]
                  return _wrap_gen(result)
                except:
                  raise RuntimeError
            else:
                raise IndexError,'list index %s out of range'%(i)
          else:
            if isinstance(i,slice):
              result=gen(_getgiacslice(self,i),<short int>self._subtype)
              return _wrap_gen(result)

            # add support for multi indexes
            elif isinstance(i,tuple):
               if(len(i)==2):
                  return self[i[0]][i[1]]
               elif(len(i)==1):
                  # in case of a tuple like this: (3,)
                  return self[i[0]]
               else:
                  return self[i[0],i[1]][tuple(i[2:])]

            else:
              raise TypeError,'gen indexes are not yet implemented'
        # Here we add support to formal variable indexes:
        else:
          cmd='%s[%s]'%(self,i)
          ans=Pygen(cmd).eval()
          # if the answer is a string, it must be an error message because self is not a list or a string
          if (ans._type == 12):
            raise TypeError, "Error executing code in Giac\nCODE:\n\t%s\nGiac ERROR:\n\t%s"%(cmd, ans)
          return ans


     def __setitem__(self,key,value):
        """
        Set the value of a coefficient of a giac vector or matrix or list.
           Warning: It is an in place affectation.


        >>> A=giac([ [ j+2*i for i in range(3)] for j in range(3)]); A
        [[0,2,4],[1,3,5],[2,4,6]]
        >>> A[1,2]=44;A
        [[0,2,4],[1,3,44],[2,4,6]]
        >>> A[2][2]=giac(1)/3;A
        [[0,2,4],[1,3,44],[2,4,1/3]]
        >>> x=giac('x')
        >>> A[0,0]=x+1/x; A
        [[x+1/x,2,4],[1,3,44],[2,4,1/3]]
        >>> A[0]=[-1,-2,-3]; A
        [[-1,-2,-3],[1,3,44],[2,4,1/3]]
        >>> B=A; A[2,2]
        1/3
        >>> B[2,2]=6    # in place affectation
        >>> A[2,2]      # so A is also modified
        6
        >>> A.pcar(x)
        x**3-8*x**2-159*x


        NB: For Large matrix it seems that the syntax A[i][j]= is faster that A[i,j]=

        >>> import giacpy
        >>> from time import time
        >>> A=giacpy.ranm(4000,4000)
        >>> t1=time(); A[500][500]=12345;t1=time()-t1
        >>> t2=time(); A[501,501]=54321;t2=time()-t2
        >>> t1,t2 # doctest: +SKIP
        (0.0002014636993408203, 0.05124521255493164)
        >>> A[500,500],A[501][501]
        (12345, 54321)

        """
        cdef gen v
        cdef gen g = gen(<string>encstring23('GIACPY_TMP_NAME050268070969290100291003'),context_ptr)
        GIAC_sto((<Pygen>self).gptr[0],g,1,context_ptr)
        g=gen(<string>encstring23('GIACPY_TMP_NAME050268070969290100291003[%s]'%(str(key))),context_ptr)
        v=(<Pygen>(Pygen(value).eval())).gptr[0]
        GIAC_sto(v,g,1,context_ptr)
        Pygen('purge(GIACPY_TMP_NAME050268070969290100291003):;').eval()
        return


     def __iter__(self):
       """
         Pygen lists of 10**6 elements should be yield

           >>> from time import clock
           >>> l=giac(range(10**6))
           >>> t=clock();l1=[ i for i in l ];t1=clock()-t;'time for a list of 10**6  i ',t1        # doctest: +ELLIPSIS
           ('time for a list of 10**6  i ', ...)
           >>> t=clock();l1=[ i+i for i in l ];t2=clock()-t;'time for a list of 10**6  i+i ',t2    # doctest: +ELLIPSIS
           ('time for a list of 10**6  i+i ', ...)
           >>> t=clock();l1=[ 1+i for i in l ];t3=clock()-t;"time for a list of 10**6  1+i ",t3    # doctest: +ELLIPSIS
           ('time for a list of 10**6  1+i ', ...)
           >>> t=clock();l1=[ i+1 for i in l ];t4=clock()-t;"time for a list of 10**6  i+1 ",t4    # doctest: +ELLIPSIS
           ('time for a list of 10**6  i+1 ', ...)

       """
       cdef int i
       #FIXME, should be improved: is it slow? and needs sig_on()?
       ressetctrl_c()
       for i in range(len(self)):
          if(GIACctrl_c):
            raise KeyboardInterrupt,"Interrupted by a ctrl-c event"
          yield self[i]

     def __int__(self):
        """
          Convert a giac integer (type Pygen in python) to  a Python <int>

            >>> a=giac('2*pi')
            >>> list(range((a.floor()).__int__()))
            [0, 1, 2, 3, 4, 5]

        """
        tmp=self.eval()
        if(tmp._type==0):
           # C int
           return tmp._val
        elif(tmp._type==2):
           # gmp int
           return int(str(tmp))
        else:
           raise TypeError,"self is not a giac integer"

     def __float__(self):
        """
           Convert a giac real to a Python <float>

             >>> a=giac('pi/4.0')
             >>> import math
             >>> math.sin(a)    # doctest: +ELLIPSIS
             0.70710678118654...
             >>> a=giac(2)
             >>> math.sqrt(a) == math.sqrt(2)
             True

        """
        # round with 14 digits should give type 1
        # but if it depends on the arch we add the type 3 test
        tmp=self.round(14).eval()
        if(tmp._type==1):
           return tmp._double
        elif(tmp._type==3):
           return float(str(tmp))
        else:
           raise TypeError,"self is not a giac real"

     def eval(self):
        cdef gen result
        ressetctrl_c()
        try:
           result=GIAC_protecteval(self.gptr[0],giacsettings.eval_level,context_ptr)
           return _wrap_gen(result)
        except:
           raise RuntimeError

     def threadeval(self,*args):
        cdef gen result
        cdef gen * param
        param=&result

        count=0
        maxcount=1000000

        n=len(args)
        if (n>1):
           right=Pygen(args).eval()
        elif (n==1):
           right=Pygen(args[0])
#        if isinstance(self,Pygen)==False:
#           self=Pygen(self)

        ressetctrl_c()

        try:
           if(n>0):
              condi=CASmakethread(GIAC_symbof((<Pygen>self).gptr[0],(<Pygen>right).gptr[0]),giacsettings.eval_level,param,context_ptr)
           else:
              condi=CASmakethread((<Pygen>self).gptr[0],giacsettings.eval_level,param,context_ptr)
           if( condi == 1):
              cont=True

              while(cont):
                   if(CASmonitor(context_ptr) == 1):
                      if(count <maxcount):
                         count=count+1

                      PyErr_CheckSignals()
                      if(testctrl_c()==1):
                         sleep(2) # try to wait if the thread stops alone
                         cont=False
                         if(CASmonitor(context_ptr) == 1):
                            print("killing thread")
                            CASkillthread(context_ptr)
                            raise KeyboardInterrupt

                      if(count >= maxcount):
                         sleep(0.05)
                      if(count >= maxcount//100):
                         sleep(0.001)
                   else:
                      cont=False

              result=param[0]
              return _wrap_gen(result)


           else:
              raise RuntimeError,"Failed to start a thread"
        except:
           setctrl_c()
           print("trying soft interruption (wait 2s)")
           sleep(2)
           print("cas monitor status:",CASmonitor(context_ptr))
           if(CASmonitor(context_ptr) == 1):
              print("warning: Killing thread")
              CASkillthread(context_ptr)
              sleep(2)
              print("cas monitor status after killing thread:",CASmonitor(context_ptr))
           raise RuntimeError


     def __add__(self, right):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         # Curiously this case is important:
         # otherwise: f=1/(2+sin(5*x)) crash
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= (<Pygen>self).gptr[0] + (<Pygen>right).gptr[0]
             return _wrap_gen(result)
         except:
             raise RuntimeError


     def __call__(self, *args):
         cdef gen result
         n=len(args)
         if (n>1):
           right=Pygen(args).eval()
         elif (n==1):
           right=Pygen(args[0])
         else:
           right=GIACNULL
         if isinstance(self,Pygen)==False:
           self=Pygen(self)
         ressetctrl_c()
         #try:
         result= ((<Pygen>self).gptr[0])((<Pygen>right).gptr[0],context_ptr)
         return _wrap_gen(result)
         #except:
         #   raise RuntimeError


     def __sub__(self, right):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= (<Pygen>self).gptr[0] - (<Pygen>right).gptr[0]
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __mul__(self, right):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             #result= (<Pygen>self).gptr[0] * (<Pygen>right).gptr[0]
             #NB: with the natural previous method, the following error generated by
             #giac causes python to quit instead of an error message.
             #l=Pygen([1,2]);l.transpose()*l;
             result= GIAC_giacmul((<Pygen>self).gptr[0] , (<Pygen>right).gptr[0],context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError

#PB / in python3 is truediv
     def __div__(self, right):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             #result= (<Pygen>self).gptr[0] / (<Pygen>right).gptr[0]
             result= GIAC_giacdiv((<Pygen>self).gptr[0] , (<Pygen>right).gptr[0], context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __truediv__(self, right):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             #result= (<Pygen>self).gptr[0] / (<Pygen>right).gptr[0]
             result= GIAC_giacdiv((<Pygen>self).gptr[0] , (<Pygen>right).gptr[0], context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError


     def __pow__(self, right ,ignored):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= GIAC_pow((<Pygen>self).gptr[0],(<Pygen>right).gptr[0], context_ptr )
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __mod__(self, right):
         cdef gen result
         if not isinstance(right,Pygen):
            right=Pygen(right)
         if not isinstance(self,Pygen):
            self=Pygen(self)
         ressetctrl_c()
         try:
             #result= gen(GIAC_makenewvecteur((<Pygen>self).gptr[0],(<Pygen>right).gptr[0]),<short int>1)
             #integer output:
             #result= GIAC_smod(result,context_ptr)
             #modular output:
             result= GIAC_giacmod((<Pygen>self).gptr[0],(<Pygen>right).gptr[0],context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __neg__(self):
         cdef gen result
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= GIAC_neg((<Pygen>self).gptr[0])
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __pos__(self):
         return self

     # To be able to use the eval function before the GiacMethods initialisation
     def cas_setup(self,*args):
        return Pygen('cas_setup')(self,*args)

     # ipython pretty printing
     def _repr_latex_(self):
        # remove quotes
        return str(self.latex())[1:-1]

     def _repr_html_(self):
        if self._type == 8:
           if self.sommet() == 'pnt':
              # no mathml output for graphics
              return None
        # remove quotes
        return str(self.mathml())[1:-1]

     #
     def save(self, str filename):
        """
          Archive a Pygen element to a file in giac compressed format.

          Use the loadgiacgen command to get back the Pygen from the file.

          In C++ these files can be opened with giac::unarchive

            >>> from giacpy import *
            >>> f=giac('(x+y+z+2)**10'); g=f.normal()
            >>> g.save("fichiertest")           #  doctest: +SKIP
            >>> a=loadgiacgen("fichiertest")    #  doctest: +SKIP
            >>> from tempfile import NamedTemporaryFile
            >>> F=NamedTemporaryFile()   # chose a temporary file for a test
            >>> Fname=F.name; F.close()  # so Fname can be our filename  
            >>> g.save(Fname)
            >>> a=loadgiacgen(Fname)
            >>> a.factor()
            (x+y+z+2)**10
            >>> F.close()

        """
        ressetctrl_c()
        try:
            GIAC_archive( <string>encstring23(filename), (<Pygen>self).gptr[0], context_ptr)
        except:
             raise RuntimeError


     def htmlhelp(self, str lang='en'):
         """
         Open the giac  html  detailled help about self in an external  browser

         There are currently 3 supported languages: 'en', 'fr', 'el'

          >>> from giacpy import gcd
          >>> gcd.htmlhelp('fr')           # doctest: +SKIP

         """
         l={'fr':1 , 'en':2, 'el':4}
         if (not lang in ['en', 'fr', 'el']):
           lang='en'
         try:
           url=decstring23(browser_help(self.gptr[0],l[lang])) #python3
           giacbasedir=decstring23(GIAC_giac_aide_dir())  # python3
         except:
           raise RuntimeError,'giac docs dir not found'
         print(url)
         if os.access(giacbasedir,os.F_OK):
            url='file:'+url
            wwwbrowseropen(url)



     def help(self):
        return self.findhelp()

     def redim(self,a,b=None):
        """
        * Increase the size of a matrix when possible, otherwise return self.

        >>> C=giac([[1,2]])
        >>> C.redim(2,3)
        [[1,2,0],[0,0,0]]
        >>> C.redim(2,1)
        [[1,2]]

        """
        d=self.dim()
        if d.type()==7:
           if(a>d[0] and b>=d[1]):
               A=self.semi_augment(Pygen((a-d[0],d[1])).matrix())
               if(b>d[1]):
                   A=A.augment(Pygen((a,b-d[1])).matrix())
               return A
           elif(b>d[1] and a==d[0]):
               return self.augment(Pygen((d[0],b-d[1])).matrix())
           else:
              return self
        else:
           raise TypeError, "self is not a giac List"


     def qcas(self,s=None):
       """
       * Send a giac graphic to qcas. (3D is currently not supported in qcas)

        >>> d1=giac('plot(x*sin(x))')
        >>> d1.qcas()    # doctest: +SKIP
        >>> l=giac([(d1*t*0.1).color(t) for t in range(10)])
        >>> l.qcas()     # doctest: +SKIP

       """
       ressetctrl_c()
       try:
          from giacpy2qcas import toqcas
          toqcas(self,s)
       except:
          raise RuntimeError


     # # # # # # # # # # # # # # # # # # # # # # # # #
     #           WARNING:
     #
     # Do not use things like != in  Pygen's __cinit__
     # with this __richcmp__ enabled
     # The methods will bug: a=Pygen(2); a.sin()
     #
     # # # # # # # # # # # # # # # # # # # # # # # # #

     def __richcmp__( self, other,op):
         if isinstance(other,Pygen)==False:
            other=Pygen(other)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= giacgenrichcmp((<Pygen>self).gptr[0],(<Pygen>other).gptr[0], op, context_ptr )
         except:
             raise RuntimeError
         if result==1 :
             return True
         else:
             return False

     #
     # Some attributes of the gen class:
     #
     property _type:
         def __get__(self):
           #if (self.gptr != NULL):
             return self.gptr.type
           #else:
           #  raise MemoryError,"This Pygen is not associated to a giac gen"


     property _subtype:
         def __get__(self):
           #if (self.gptr != NULL):
             return self.gptr.subtype
           #else:
           #  raise MemoryError,"This Pygen is not associated to a giac gen"


     property _val:  # immediate int (type _INT_)
         """
         immediate int value of an _INT_ type gen.
         """
         def __get__(self):
           #if (self.gptr != NULL):
             return self.gptr.val
           #else:
           #  raise MemoryError,"This Pygen is not associated to a giac gen"


     property _double:  # immediate double (type _DOUBLE_)
         """
         immediate conversion to float for a gen of _DOUBLE_ type.
         """
         def __get__(self):
           #if (self.gptr != NULL):
             return self.gptr._DOUBLE_val
           #else:
           #  raise MemoryError,"This Pygen is not associated to a giac gen."


     property help:
         def __get__(self):
           return self.help()

     ###################################################
     # Add the others methods
     ###################################################
     #
     #  NB: with __getattr__ this is about 10 times slower: [a.normal() for i in range(10**4)]
     #      than [GiacMethods["normal"](a) for i in range(10**4)]
     #
     #     def __getattr__(self, name):
     #       return GiacMethods[str(name)](self)
     ##
     def Airy_Ai(self,*args):
        return GiacMethods['Airy_Ai'](self,*args)

     def Airy_Bi(self,*args):
        return GiacMethods['Airy_Bi'](self,*args)

     def Archive(self,*args):
        return GiacMethods['Archive'](self,*args)

     def BesselJ(self,*args):
        return GiacMethods['BesselJ'](self,*args)

     def BesselY(self,*args):
        return GiacMethods['BesselY'](self,*args)

     def Beta(self,*args):
        return GiacMethods['Beta'](self,*args)

     def BlockDiagonal(self,*args):
        return GiacMethods['BlockDiagonal'](self,*args)

     def Ci(self,*args):
        return GiacMethods['Ci'](self,*args)

     def Circle(self,*args):
        return GiacMethods['Circle'](self,*args)

     def Col(self,*args):
        return GiacMethods['Col'](self,*args)

     def CopyVar(self,*args):
        return GiacMethods['CopyVar'](self,*args)

     def Dirac(self,*args):
        return GiacMethods['Dirac'](self,*args)

     def Ei(self,*args):
        return GiacMethods['Ei'](self,*args)

     def Factor(self,*args):
        return GiacMethods['Factor'](self,*args)

     def GF(self,*args):
        return GiacMethods['GF'](self,*args)

     def Gamma(self,*args):
        return GiacMethods['Gamma'](self,*args)

     def Heaviside(self,*args):
        return GiacMethods['Heaviside'](self,*args)

     def JordanBlock(self,*args):
        return GiacMethods['JordanBlock'](self,*args)

     def LU(self,*args):
        return GiacMethods['LU'](self,*args)

     def Li(self,*args):
        return GiacMethods['Li'](self,*args)

     def Line(self,*args):
        return GiacMethods['Line'](self,*args)

     def LineHorz(self,*args):
        return GiacMethods['LineHorz'](self,*args)

     def LineTan(self,*args):
        return GiacMethods['LineTan'](self,*args)

     def LineVert(self,*args):
        return GiacMethods['LineVert'](self,*args)

     def Phi(self,*args):
        return GiacMethods['Phi'](self,*args)

     def Pi(self,*args):
        return GiacMethods['Pi'](self,*args)

     def Psi(self,*args):
        return GiacMethods['Psi'](self,*args)

     def QR(self,*args):
        return GiacMethods['QR'](self,*args)

     def RandSeed(self,*args):
        return GiacMethods['RandSeed'](self,*args)

     def Row(self,*args):
        return GiacMethods['Row'](self,*args)

     def SortA(self,*args):
        return GiacMethods['SortA'](self,*args)

     def SortD(self,*args):
        return GiacMethods['SortD'](self,*args)

     def UTPC(self,*args):
        return GiacMethods['UTPC'](self,*args)

     def UTPF(self,*args):
        return GiacMethods['UTPF'](self,*args)

     def UTPN(self,*args):
        return GiacMethods['UTPN'](self,*args)

     def UTPT(self,*args):
        return GiacMethods['UTPT'](self,*args)

     def VARS(self,*args):
        return GiacMethods['VARS'](self,*args)

     def VAS(self,*args):
        return GiacMethods['VAS'](self,*args)

     def VAS_positive(self,*args):
        return GiacMethods['VAS_positive'](self,*args)

     def Zeta(self,*args):
        return GiacMethods['Zeta'](self,*args)

     def a2q(self,*args):
        return GiacMethods['a2q'](self,*args)

     def abcuv(self,*args):
        return GiacMethods['abcuv'](self,*args)

     def about(self,*args):
        return GiacMethods['about'](self,*args)

     def abs(self,*args):
        return GiacMethods['abs'](self,*args)

     def abscissa(self,*args):
        return GiacMethods['abscissa'](self,*args)

     def accumulate_head_tail(self,*args):
        return GiacMethods['accumulate_head_tail'](self,*args)

     def acos(self,*args):
        return GiacMethods['acos'](self,*args)

     def acos2asin(self,*args):
        return GiacMethods['acos2asin'](self,*args)

     def acos2atan(self,*args):
        return GiacMethods['acos2atan'](self,*args)

     def acosh(self,*args):
        return GiacMethods['acosh'](self,*args)

     def acot(self,*args):
        return GiacMethods['acot'](self,*args)

     def acsc(self,*args):
        return GiacMethods['acsc'](self,*args)

     def add(self,*args):
        return GiacMethods['add'](self,*args)

     def additionally(self,*args):
        return GiacMethods['additionally'](self,*args)

     def adjoint_matrix(self,*args):
        return GiacMethods['adjoint_matrix'](self,*args)

     def affix(self,*args):
        return GiacMethods['affix'](self,*args)

     def algsubs(self,*args):
        return GiacMethods['algsubs'](self,*args)

     def algvar(self,*args):
        return GiacMethods['algvar'](self,*args)

     def alog10(self,*args):
        return GiacMethods['alog10'](self,*args)

     def altitude(self,*args):
        return GiacMethods['altitude'](self,*args)

     def angle(self,*args):
        return GiacMethods['angle'](self,*args)

     def angle_radian(self,*args):
        return GiacMethods['angle_radian'](self,*args)

     def angleat(self,*args):
        return GiacMethods['angleat'](self,*args)

     def angleatraw(self,*args):
        return GiacMethods['angleatraw'](self,*args)

     def ans(self,*args):
        return GiacMethods['ans'](self,*args)

     def apply(self,*args):
        return GiacMethods['apply'](self,*args)

     def approx(self,*args):
        return GiacMethods['approx'](self,*args)

     def arc(self,*args):
        return GiacMethods['arc'](self,*args)

     def arcLen(self,*args):
        return GiacMethods['arcLen'](self,*args)

     def arccos(self,*args):
        return GiacMethods['arccos'](self,*args)

     def arccosh(self,*args):
        return GiacMethods['arccosh'](self,*args)

     def arclen(self,*args):
        return GiacMethods['arclen'](self,*args)

     def arcsin(self,*args):
        return GiacMethods['arcsin'](self,*args)

     def arcsinh(self,*args):
        return GiacMethods['arcsinh'](self,*args)

     def arctan(self,*args):
        return GiacMethods['arctan'](self,*args)

     def arctanh(self,*args):
        return GiacMethods['arctanh'](self,*args)

     def area(self,*args):
        return GiacMethods['area'](self,*args)

     def areaat(self,*args):
        return GiacMethods['areaat'](self,*args)

     def areaatraw(self,*args):
        return GiacMethods['areaatraw'](self,*args)

     def areaplot(self,*args):
        return GiacMethods['areaplot'](self,*args)

     def arg(self,*args):
        return GiacMethods['arg'](self,*args)

     def array(self,*args):
        return GiacMethods['array'](self,*args)

     def asin(self,*args):
        return GiacMethods['asin'](self,*args)

     def asin2acos(self,*args):
        return GiacMethods['asin2acos'](self,*args)

     def asin2atan(self,*args):
        return GiacMethods['asin2atan'](self,*args)

     def asinh(self,*args):
        return GiacMethods['asinh'](self,*args)

     def assume(self,*args):
        return GiacMethods['assume'](self,*args)

     def at(self,*args):
        return GiacMethods['at'](self,*args)

     def atan(self,*args):
        return GiacMethods['atan'](self,*args)

     def atan2acos(self,*args):
        return GiacMethods['atan2acos'](self,*args)

     def atan2asin(self,*args):
        return GiacMethods['atan2asin'](self,*args)

     def atanh(self,*args):
        return GiacMethods['atanh'](self,*args)

     def atrig2ln(self,*args):
        return GiacMethods['atrig2ln'](self,*args)

     def augment(self,*args):
        return GiacMethods['augment'](self,*args)

     def autosimplify(self,*args):
        return GiacMethods['autosimplify'](self,*args)

     def avance(self,*args):
        return GiacMethods['avance'](self,*args)

     def avgRC(self,*args):
        return GiacMethods['avgRC'](self,*args)

     def axes(self,*args):
        return GiacMethods['axes'](self,*args)

     def back(self,*args):
        return GiacMethods['back'](self,*args)

     def baisse_crayon(self,*args):
        return GiacMethods['baisse_crayon'](self,*args)

     def bar_plot(self,*args):
        return GiacMethods['bar_plot'](self,*args)

     def barycenter(self,*args):
        return GiacMethods['barycenter'](self,*args)

     def base(self,*args):
        return GiacMethods['base'](self,*args)

     def basis(self,*args):
        return GiacMethods['basis'](self,*args)

     def batons(self,*args):
        return GiacMethods['batons'](self,*args)

     def bernoulli(self,*args):
        return GiacMethods['bernoulli'](self,*args)

     def besselJ(self,*args):
        return GiacMethods['besselJ'](self,*args)

     def besselY(self,*args):
        return GiacMethods['besselY'](self,*args)

     def betad(self,*args):
        return GiacMethods['betad'](self,*args)

     def betad_cdf(self,*args):
        return GiacMethods['betad_cdf'](self,*args)

     def betad_icdf(self,*args):
        return GiacMethods['betad_icdf'](self,*args)

     def bezier(self,*args):
        return GiacMethods['bezier'](self,*args)

     def bezout_entiers(self,*args):
        return GiacMethods['bezout_entiers'](self,*args)

     def binomial(self,*args):
        return GiacMethods['binomial'](self,*args)

     def binomial_cdf(self,*args):
        return GiacMethods['binomial_cdf'](self,*args)

     def binomial_icdf(self,*args):
        return GiacMethods['binomial_icdf'](self,*args)

     def bisection_solver(self,*args):
        return GiacMethods['bisection_solver'](self,*args)

     def bisector(self,*args):
        return GiacMethods['bisector'](self,*args)

     def bitand(self,*args):
        return GiacMethods['bitand'](self,*args)

     def bitor(self,*args):
        return GiacMethods['bitor'](self,*args)

     def bitxor(self,*args):
        return GiacMethods['bitxor'](self,*args)

     def blockmatrix(self,*args):
        return GiacMethods['blockmatrix'](self,*args)

     def border(self,*args):
        return GiacMethods['border'](self,*args)

     def boxwhisker(self,*args):
        return GiacMethods['boxwhisker'](self,*args)

     def brent_solver(self,*args):
        return GiacMethods['brent_solver'](self,*args)

     def cFactor(self,*args):
        return GiacMethods['cFactor'](self,*args)

     def cSolve(self,*args):
        return GiacMethods['cSolve'](self,*args)

     def cZeros(self,*args):
        return GiacMethods['cZeros'](self,*args)

     def camembert(self,*args):
        return GiacMethods['camembert'](self,*args)

     def canonical_form(self,*args):
        return GiacMethods['canonical_form'](self,*args)

     def cauchy(self,*args):
        return GiacMethods['cauchy'](self,*args)

     def cauchy_cdf(self,*args):
        return GiacMethods['cauchy_cdf'](self,*args)

     def cauchy_icdf(self,*args):
        return GiacMethods['cauchy_icdf'](self,*args)

     def cauchyd(self,*args):
        return GiacMethods['cauchyd'](self,*args)

     def cauchyd_cdf(self,*args):
        return GiacMethods['cauchyd_cdf'](self,*args)

     def cauchyd_icdf(self,*args):
        return GiacMethods['cauchyd_icdf'](self,*args)

     def cdf(self,*args):
        return GiacMethods['cdf'](self,*args)

     def ceil(self,*args):
        return GiacMethods['ceil'](self,*args)

     def ceiling(self,*args):
        return GiacMethods['ceiling'](self,*args)

     def center(self,*args):
        return GiacMethods['center'](self,*args)

     def center2interval(self,*args):
        return GiacMethods['center2interval'](self,*args)

     def centered_cube(self,*args):
        return GiacMethods['centered_cube'](self,*args)

     def centered_tetrahedron(self,*args):
        return GiacMethods['centered_tetrahedron'](self,*args)

     def cfactor(self,*args):
        return GiacMethods['cfactor'](self,*args)

     def cfsolve(self,*args):
        return GiacMethods['cfsolve'](self,*args)

     def changebase(self,*args):
        return GiacMethods['changebase'](self,*args)

     def char(self,*args):
        return GiacMethods['char'](self,*args)

     def charpoly(self,*args):
        return GiacMethods['charpoly'](self,*args)

     def chinrem(self,*args):
        return GiacMethods['chinrem'](self,*args)

     def chisquare(self,*args):
        return GiacMethods['chisquare'](self,*args)

     def chisquare_cdf(self,*args):
        return GiacMethods['chisquare_cdf'](self,*args)

     def chisquare_icdf(self,*args):
        return GiacMethods['chisquare_icdf'](self,*args)

     def chisquared(self,*args):
        return GiacMethods['chisquared'](self,*args)

     def chisquared_cdf(self,*args):
        return GiacMethods['chisquared_cdf'](self,*args)

     def chisquared_icdf(self,*args):
        return GiacMethods['chisquared_icdf'](self,*args)

     def chisquaret(self,*args):
        return GiacMethods['chisquaret'](self,*args)

     def cholesky(self,*args):
        return GiacMethods['cholesky'](self,*args)

     def chrem(self,*args):
        return GiacMethods['chrem'](self,*args)

     def circle(self,*args):
        return GiacMethods['circle'](self,*args)

     def circumcircle(self,*args):
        return GiacMethods['circumcircle'](self,*args)

     def classes(self,*args):
        return GiacMethods['classes'](self,*args)

     def coeff(self,*args):
        return GiacMethods['coeff'](self,*args)

     def coeffs(self,*args):
        return GiacMethods['coeffs'](self,*args)

     def col(self,*args):
        return GiacMethods['col'](self,*args)

     def colDim(self,*args):
        return GiacMethods['colDim'](self,*args)

     def colNorm(self,*args):
        return GiacMethods['colNorm'](self,*args)

     def colSwap(self,*args):
        return GiacMethods['colSwap'](self,*args)

     def coldim(self,*args):
        return GiacMethods['coldim'](self,*args)

     def collect(self,*args):
        return GiacMethods['collect'](self,*args)

     def colnorm(self,*args):
        return GiacMethods['colnorm'](self,*args)

     def color(self,*args):
        return GiacMethods['color'](self,*args)

     def colspace(self,*args):
        return GiacMethods['colspace'](self,*args)

     def colswap(self,*args):
        return GiacMethods['colswap'](self,*args)

     def comDenom(self,*args):
        return GiacMethods['comDenom'](self,*args)

     def comb(self,*args):
        return GiacMethods['comb'](self,*args)

     def combine(self,*args):
        return GiacMethods['combine'](self,*args)

     def comment(self,*args):
        return GiacMethods['comment'](self,*args)

     def common_perpendicular(self,*args):
        return GiacMethods['common_perpendicular'](self,*args)

     def companion(self,*args):
        return GiacMethods['companion'](self,*args)

     def compare(self,*args):
        return GiacMethods['compare'](self,*args)

     def complex(self,*args):
        return GiacMethods['complex'](self,*args)

     def complex_variables(self,*args):
        return GiacMethods['complex_variables'](self,*args)

     def complexroot(self,*args):
        return GiacMethods['complexroot'](self,*args)

     def concat(self,*args):
        return GiacMethods['concat'](self,*args)

     def cond(self,*args):
        return GiacMethods['cond'](self,*args)

     def cone(self,*args):
        return GiacMethods['cone'](self,*args)

     def confrac(self,*args):
        return GiacMethods['confrac'](self,*args)

     def conic(self,*args):
        return GiacMethods['conic'](self,*args)

     def conj(self,*args):
        return GiacMethods['conj'](self,*args)

     def conjugate_gradient(self,*args):
        return GiacMethods['conjugate_gradient'](self,*args)

     def cont(self,*args):
        return GiacMethods['cont'](self,*args)

     def contains(self,*args):
        return GiacMethods['contains'](self,*args)

     def content(self,*args):
        return GiacMethods['content'](self,*args)

     def contourplot(self,*args):
        return GiacMethods['contourplot'](self,*args)

     def convert(self,*args):
        return GiacMethods['convert'](self,*args)

     def convertir(self,*args):
        return GiacMethods['convertir'](self,*args)

     def convexhull(self,*args):
        return GiacMethods['convexhull'](self,*args)

     def coordinates(self,*args):
        return GiacMethods['coordinates'](self,*args)

     def copy(self,*args):
        return GiacMethods['copy'](self,*args)

     def correlation(self,*args):
        return GiacMethods['correlation'](self,*args)

     def cos(self,*args):
        return GiacMethods['cos'](self,*args)

     def cos2sintan(self,*args):
        return GiacMethods['cos2sintan'](self,*args)

     def cosh(self,*args):
        return GiacMethods['cosh'](self,*args)

     def cot(self,*args):
        return GiacMethods['cot'](self,*args)

     def cote(self,*args):
        return GiacMethods['cote'](self,*args)

     def count(self,*args):
        return GiacMethods['count'](self,*args)

     def count_eq(self,*args):
        return GiacMethods['count_eq'](self,*args)

     def count_inf(self,*args):
        return GiacMethods['count_inf'](self,*args)

     def count_sup(self,*args):
        return GiacMethods['count_sup'](self,*args)

     def courbe_parametrique(self,*args):
        return GiacMethods['courbe_parametrique'](self,*args)

     def courbe_polaire(self,*args):
        return GiacMethods['courbe_polaire'](self,*args)

     def covariance(self,*args):
        return GiacMethods['covariance'](self,*args)

     def covariance_correlation(self,*args):
        return GiacMethods['covariance_correlation'](self,*args)

     def cpartfrac(self,*args):
        return GiacMethods['cpartfrac'](self,*args)

     def crationalroot(self,*args):
        return GiacMethods['crationalroot'](self,*args)

     def crayon(self,*args):
        return GiacMethods['crayon'](self,*args)

     def cross(self,*args):
        return GiacMethods['cross'](self,*args)

     def crossP(self,*args):
        return GiacMethods['crossP'](self,*args)

     def cross_point(self,*args):
        return GiacMethods['cross_point'](self,*args)

     def cross_ratio(self,*args):
        return GiacMethods['cross_ratio'](self,*args)

     def crossproduct(self,*args):
        return GiacMethods['crossproduct'](self,*args)

     def csc(self,*args):
        return GiacMethods['csc'](self,*args)

     def csolve(self,*args):
        return GiacMethods['csolve'](self,*args)

     def cube(self,*args):
        return GiacMethods['cube'](self,*args)

     def cumSum(self,*args):
        return GiacMethods['cumSum'](self,*args)

     def cumsum(self,*args):
        return GiacMethods['cumsum'](self,*args)

     def cumulated_frequencies(self,*args):
        return GiacMethods['cumulated_frequencies'](self,*args)

     def curl(self,*args):
        return GiacMethods['curl'](self,*args)

     def current_sheet(self,*args):
        return GiacMethods['current_sheet'](self,*args)

     def curvature(self,*args):
        return GiacMethods['curvature'](self,*args)

     def curve(self,*args):
        return GiacMethods['curve'](self,*args)

     def cyan(self,*args):
        return GiacMethods['cyan'](self,*args)

     def cycle2perm(self,*args):
        return GiacMethods['cycle2perm'](self,*args)

     def cycleinv(self,*args):
        return GiacMethods['cycleinv'](self,*args)

     def cycles2permu(self,*args):
        return GiacMethods['cycles2permu'](self,*args)

     def cyclotomic(self,*args):
        return GiacMethods['cyclotomic'](self,*args)

     def cylinder(self,*args):
        return GiacMethods['cylinder'](self,*args)

     def dash_line(self,*args):
        return GiacMethods['dash_line'](self,*args)

     def dashdot_line(self,*args):
        return GiacMethods['dashdot_line'](self,*args)

     def dashdotdot_line(self,*args):
        return GiacMethods['dashdotdot_line'](self,*args)

     def dayofweek(self,*args):
        return GiacMethods['dayofweek'](self,*args)

     def deSolve(self,*args):
        return GiacMethods['deSolve'](self,*args)

     def debut_enregistrement(self,*args):
        return GiacMethods['debut_enregistrement'](self,*args)

     def degree(self,*args):
        return GiacMethods['degree'](self,*args)

     def delcols(self,*args):
        return GiacMethods['delcols'](self,*args)

     def delrows(self,*args):
        return GiacMethods['delrows'](self,*args)

     def deltalist(self,*args):
        return GiacMethods['deltalist'](self,*args)

     def denom(self,*args):
        return GiacMethods['denom'](self,*args)

     def densityplot(self,*args):
        return GiacMethods['densityplot'](self,*args)

     def derive(self,*args):
        return GiacMethods['derive'](self,*args)

     def deriver(self,*args):
        return GiacMethods['deriver'](self,*args)

     def desolve(self,*args):
        return GiacMethods['desolve'](self,*args)

     def dessine_tortue(self,*args):
        return GiacMethods['dessine_tortue'](self,*args)

     def det(self,*args):
        return GiacMethods['det'](self,*args)

     def det_minor(self,*args):
        return GiacMethods['det_minor'](self,*args)

     def developper(self,*args):
        return GiacMethods['developper'](self,*args)

     def developper_transcendant(self,*args):
        return GiacMethods['developper_transcendant'](self,*args)

     def dfc(self,*args):
        return GiacMethods['dfc'](self,*args)

     def dfc2f(self,*args):
        return GiacMethods['dfc2f'](self,*args)

     def diag(self,*args):
        return GiacMethods['diag'](self,*args)

     def diff(self,*args):
        return GiacMethods['diff'](self,*args)

     def dim(self,*args):
        return GiacMethods['dim'](self,*args)

     def display(self,*args):
        return GiacMethods['display'](self,*args)

     def disque(self,*args):
        return GiacMethods['disque'](self,*args)

     def disque_centre(self,*args):
        return GiacMethods['disque_centre'](self,*args)

     def distance(self,*args):
        return GiacMethods['distance'](self,*args)

     def distance2(self,*args):
        return GiacMethods['distance2'](self,*args)

     def distanceat(self,*args):
        return GiacMethods['distanceat'](self,*args)

     def distanceatraw(self,*args):
        return GiacMethods['distanceatraw'](self,*args)

     def divergence(self,*args):
        return GiacMethods['divergence'](self,*args)

     def divide(self,*args):
        return GiacMethods['divide'](self,*args)

     def divis(self,*args):
        return GiacMethods['divis'](self,*args)

     def division_point(self,*args):
        return GiacMethods['division_point'](self,*args)

     def divisors(self,*args):
        return GiacMethods['divisors'](self,*args)

     def divpc(self,*args):
        return GiacMethods['divpc'](self,*args)

     def dnewton_solver(self,*args):
        return GiacMethods['dnewton_solver'](self,*args)

     def dodecahedron(self,*args):
        return GiacMethods['dodecahedron'](self,*args)

     def dot(self,*args):
        return GiacMethods['dot'](self,*args)

     def dotP(self,*args):
        return GiacMethods['dotP'](self,*args)

     def dot_paper(self,*args):
        return GiacMethods['dot_paper'](self,*args)

     def dotprod(self,*args):
        return GiacMethods['dotprod'](self,*args)

     def droit(self,*args):
        return GiacMethods['droit'](self,*args)

     def droite_tangente(self,*args):
        return GiacMethods['droite_tangente'](self,*args)

     def dsolve(self,*args):
        return GiacMethods['dsolve'](self,*args)

     def e(self,*args):
        return GiacMethods['e'](self,*args)

     def e2r(self,*args):
        return GiacMethods['e2r'](self,*args)

     def ecart_type(self,*args):
        return GiacMethods['ecart_type'](self,*args)

     def ecart_type_population(self,*args):
        return GiacMethods['ecart_type_population'](self,*args)

     def egcd(self,*args):
        return GiacMethods['egcd'](self,*args)

     def egv(self,*args):
        return GiacMethods['egv'](self,*args)

     def egvl(self,*args):
        return GiacMethods['egvl'](self,*args)

     def eigVc(self,*args):
        return GiacMethods['eigVc'](self,*args)

     def eigVl(self,*args):
        return GiacMethods['eigVl'](self,*args)

     def eigenvals(self,*args):
        return GiacMethods['eigenvals'](self,*args)

     def eigenvalues(self,*args):
        return GiacMethods['eigenvalues'](self,*args)

     def eigenvectors(self,*args):
        return GiacMethods['eigenvectors'](self,*args)

     def eigenvects(self,*args):
        return GiacMethods['eigenvects'](self,*args)

     def element(self,*args):
        return GiacMethods['element'](self,*args)

     def eliminate(self,*args):
        return GiacMethods['eliminate'](self,*args)

     def ellipse(self,*args):
        return GiacMethods['ellipse'](self,*args)

     def entry(self,*args):
        return GiacMethods['entry'](self,*args)

     def envelope(self,*args):
        return GiacMethods['envelope'](self,*args)

     def epsilon(self,*args):
        return GiacMethods['epsilon'](self,*args)

     def epsilon2zero(self,*args):
        return GiacMethods['epsilon2zero'](self,*args)

     def equal(self,*args):
        return GiacMethods['equal'](self,*args)

     def equal2diff(self,*args):
        return GiacMethods['equal2diff'](self,*args)

     def equal2list(self,*args):
        return GiacMethods['equal2list'](self,*args)

     def equation(self,*args):
        return GiacMethods['equation'](self,*args)

     def equilateral_triangle(self,*args):
        return GiacMethods['equilateral_triangle'](self,*args)

     def erf(self,*args):
        return GiacMethods['erf'](self,*args)

     def erfc(self,*args):
        return GiacMethods['erfc'](self,*args)

     def error(self,*args):
        return GiacMethods['error'](self,*args)

     def euler(self,*args):
        return GiacMethods['euler'](self,*args)

     def euler_gamma(self,*args):
        return GiacMethods['euler_gamma'](self,*args)

     def eval_level(self,*args):
        return GiacMethods['eval_level'](self,*args)

     def evala(self,*args):
        return GiacMethods['evala'](self,*args)

     def evalb(self,*args):
        return GiacMethods['evalb'](self,*args)

     def evalc(self,*args):
        return GiacMethods['evalc'](self,*args)

     def evalf(self,*args):
        return GiacMethods['evalf'](self,*args)

     def evalm(self,*args):
        return GiacMethods['evalm'](self,*args)

     def even(self,*args):
        return GiacMethods['even'](self,*args)

     def evolute(self,*args):
        return GiacMethods['evolute'](self,*args)

     def exact(self,*args):
        return GiacMethods['exact'](self,*args)

     def exbisector(self,*args):
        return GiacMethods['exbisector'](self,*args)

     def excircle(self,*args):
        return GiacMethods['excircle'](self,*args)

     def execute(self,*args):
        return GiacMethods['execute'](self,*args)

     def exp(self,*args):
        return GiacMethods['exp'](self,*args)

     def exp2list(self,*args):
        return GiacMethods['exp2list'](self,*args)

     def exp2pow(self,*args):
        return GiacMethods['exp2pow'](self,*args)

     def exp2trig(self,*args):
        return GiacMethods['exp2trig'](self,*args)

     def expand(self,*args):
        return GiacMethods['expand'](self,*args)

     def expexpand(self,*args):
        return GiacMethods['expexpand'](self,*args)

     def expln(self,*args):
        return GiacMethods['expln'](self,*args)

     def exponential(self,*args):
        return GiacMethods['exponential'](self,*args)

     def exponential_cdf(self,*args):
        return GiacMethods['exponential_cdf'](self,*args)

     def exponential_icdf(self,*args):
        return GiacMethods['exponential_icdf'](self,*args)

     def exponential_regression(self,*args):
        return GiacMethods['exponential_regression'](self,*args)

     def exponential_regression_plot(self,*args):
        return GiacMethods['exponential_regression_plot'](self,*args)

     def exponentiald(self,*args):
        return GiacMethods['exponentiald'](self,*args)

     def exponentiald_cdf(self,*args):
        return GiacMethods['exponentiald_cdf'](self,*args)

     def exponentiald_icdf(self,*args):
        return GiacMethods['exponentiald_icdf'](self,*args)

     def expr(self,*args):
        return GiacMethods['expr'](self,*args)

     def extract_measure(self,*args):
        return GiacMethods['extract_measure'](self,*args)

     def ezgcd(self,*args):
        return GiacMethods['ezgcd'](self,*args)

     def f2nd(self,*args):
        return GiacMethods['f2nd'](self,*args)

     def fMax(self,*args):
        return GiacMethods['fMax'](self,*args)

     def fMin(self,*args):
        return GiacMethods['fMin'](self,*args)

     def fPart(self,*args):
        return GiacMethods['fPart'](self,*args)

     def faces(self,*args):
        return GiacMethods['faces'](self,*args)

     def facteurs_premiers(self,*args):
        return GiacMethods['facteurs_premiers'](self,*args)

     def factor(self,*args):
        return GiacMethods['factor'](self,*args)

     def factor_xn(self,*args):
        return GiacMethods['factor_xn'](self,*args)

     def factorial(self,*args):
        return GiacMethods['factorial'](self,*args)

     def factoriser(self,*args):
        return GiacMethods['factoriser'](self,*args)

     def factoriser_entier(self,*args):
        return GiacMethods['factoriser_entier'](self,*args)

     def factoriser_sur_C(self,*args):
        return GiacMethods['factoriser_sur_C'](self,*args)

     def factors(self,*args):
        return GiacMethods['factors'](self,*args)

     def fadeev(self,*args):
        return GiacMethods['fadeev'](self,*args)

     def false(self,*args):
        return GiacMethods['false'](self,*args)

     def falsepos_solver(self,*args):
        return GiacMethods['falsepos_solver'](self,*args)

     def fclose(self,*args):
        return GiacMethods['fclose'](self,*args)

     def fcoeff(self,*args):
        return GiacMethods['fcoeff'](self,*args)

     def fdistrib(self,*args):
        return GiacMethods['fdistrib'](self,*args)

     def fft(self,*args):
        return GiacMethods['fft'](self,*args)

     def fieldplot(self,*args):
        return GiacMethods['fieldplot'](self,*args)

     def find(self,*args):
        return GiacMethods['find'](self,*args)

     def findhelp(self,*args):
        return GiacMethods['findhelp'](self,*args)

     def fisher(self,*args):
        return GiacMethods['fisher'](self,*args)

     def fisher_cdf(self,*args):
        return GiacMethods['fisher_cdf'](self,*args)

     def fisher_icdf(self,*args):
        return GiacMethods['fisher_icdf'](self,*args)

     def fisherd(self,*args):
        return GiacMethods['fisherd'](self,*args)

     def fisherd_cdf(self,*args):
        return GiacMethods['fisherd_cdf'](self,*args)

     def fisherd_icdf(self,*args):
        return GiacMethods['fisherd_icdf'](self,*args)

     def flatten(self,*args):
        return GiacMethods['flatten'](self,*args)

     def float2rational(self,*args):
        return GiacMethods['float2rational'](self,*args)

     def floor(self,*args):
        return GiacMethods['floor'](self,*args)

     def fonction_derivee(self,*args):
        return GiacMethods['fonction_derivee'](self,*args)

     def fourier_an(self,*args):
        return GiacMethods['fourier_an'](self,*args)

     def fourier_bn(self,*args):
        return GiacMethods['fourier_bn'](self,*args)

     def fourier_cn(self,*args):
        return GiacMethods['fourier_cn'](self,*args)

     def fprint(self,*args):
        return GiacMethods['fprint'](self,*args)

     def frac(self,*args):
        return GiacMethods['frac'](self,*args)

     def fracmod(self,*args):
        return GiacMethods['fracmod'](self,*args)

     def frame_2d(self,*args):
        return GiacMethods['frame_2d'](self,*args)

     def frequencies(self,*args):
        return GiacMethods['frequencies'](self,*args)

     def frobenius_norm(self,*args):
        return GiacMethods['frobenius_norm'](self,*args)

     def froot(self,*args):
        return GiacMethods['froot'](self,*args)

     def fsolve(self,*args):
        return GiacMethods['fsolve'](self,*args)

     def fullparfrac(self,*args):
        return GiacMethods['fullparfrac'](self,*args)

     def funcplot(self,*args):
        return GiacMethods['funcplot'](self,*args)

     def function_diff(self,*args):
        return GiacMethods['function_diff'](self,*args)

     def fxnd(self,*args):
        return GiacMethods['fxnd'](self,*args)

     def gammad(self,*args):
        return GiacMethods['gammad'](self,*args)

     def gammad_cdf(self,*args):
        return GiacMethods['gammad_cdf'](self,*args)

     def gammad_icdf(self,*args):
        return GiacMethods['gammad_icdf'](self,*args)

     def gauss(self,*args):
        return GiacMethods['gauss'](self,*args)

     def gauss15(self,*args):
        return GiacMethods['gauss15'](self,*args)

     def gauss_seidel_linsolve(self,*args):
        return GiacMethods['gauss_seidel_linsolve'](self,*args)

     def gaussjord(self,*args):
        return GiacMethods['gaussjord'](self,*args)

     def gaussquad(self,*args):
        return GiacMethods['gaussquad'](self,*args)

     def gbasis(self,*args):
        return GiacMethods['gbasis'](self,*args)

     def gcd(self,*args):
        return GiacMethods['gcd'](self,*args)

     def gcdex(self,*args):
        return GiacMethods['gcdex'](self,*args)

     def genpoly(self,*args):
        return GiacMethods['genpoly'](self,*args)

     def geometric(self,*args):
        return GiacMethods['geometric'](self,*args)

     def geometric_cdf(self,*args):
        return GiacMethods['geometric_cdf'](self,*args)

     def geometric_icdf(self,*args):
        return GiacMethods['geometric_icdf'](self,*args)

     def getDenom(self,*args):
        return GiacMethods['getDenom'](self,*args)

     def getKey(self,*args):
        return GiacMethods['getKey'](self,*args)

     def getNum(self,*args):
        return GiacMethods['getNum'](self,*args)

     def getType(self,*args):
        return GiacMethods['getType'](self,*args)

     def greduce(self,*args):
        return GiacMethods['greduce'](self,*args)

     def groupermu(self,*args):
        return GiacMethods['groupermu'](self,*args)

     def hadamard(self,*args):
        return GiacMethods['hadamard'](self,*args)

     def half_cone(self,*args):
        return GiacMethods['half_cone'](self,*args)

     def half_line(self,*args):
        return GiacMethods['half_line'](self,*args)

     def halftan(self,*args):
        return GiacMethods['halftan'](self,*args)

     def halftan_hyp2exp(self,*args):
        return GiacMethods['halftan_hyp2exp'](self,*args)

     def halt(self,*args):
        return GiacMethods['halt'](self,*args)

     def hamdist(self,*args):
        return GiacMethods['hamdist'](self,*args)

     def harmonic_conjugate(self,*args):
        return GiacMethods['harmonic_conjugate'](self,*args)

     def harmonic_division(self,*args):
        return GiacMethods['harmonic_division'](self,*args)

     def has(self,*args):
        return GiacMethods['has'](self,*args)

     def hasard(self,*args):
        return GiacMethods['hasard'](self,*args)

     def head(self,*args):
        return GiacMethods['head'](self,*args)

     def hermite(self,*args):
        return GiacMethods['hermite'](self,*args)

     def hessenberg(self,*args):
        return GiacMethods['hessenberg'](self,*args)

     def hessian(self,*args):
        return GiacMethods['hessian'](self,*args)

     def heugcd(self,*args):
        return GiacMethods['heugcd'](self,*args)

     def hexagon(self,*args):
        return GiacMethods['hexagon'](self,*args)

     def hilbert(self,*args):
        return GiacMethods['hilbert'](self,*args)

     def histogram(self,*args):
        return GiacMethods['histogram'](self,*args)

     def hold(self,*args):
        return GiacMethods['hold'](self,*args)

     def homothety(self,*args):
        return GiacMethods['homothety'](self,*args)

     def horner(self,*args):
        return GiacMethods['horner'](self,*args)

     def hybrid_solver(self,*args):
        return GiacMethods['hybrid_solver'](self,*args)

     def hybridj_solver(self,*args):
        return GiacMethods['hybridj_solver'](self,*args)

     def hybrids_solver(self,*args):
        return GiacMethods['hybrids_solver'](self,*args)

     def hybridsj_solver(self,*args):
        return GiacMethods['hybridsj_solver'](self,*args)

     def hyp2exp(self,*args):
        return GiacMethods['hyp2exp'](self,*args)

     def hyperbola(self,*args):
        return GiacMethods['hyperbola'](self,*args)

     def iPart(self,*args):
        return GiacMethods['iPart'](self,*args)

     def iabcuv(self,*args):
        return GiacMethods['iabcuv'](self,*args)

     def ibasis(self,*args):
        return GiacMethods['ibasis'](self,*args)

     def ibpdv(self,*args):
        return GiacMethods['ibpdv'](self,*args)

     def ibpu(self,*args):
        return GiacMethods['ibpu'](self,*args)

     def icdf(self,*args):
        return GiacMethods['icdf'](self,*args)

     def ichinrem(self,*args):
        return GiacMethods['ichinrem'](self,*args)

     def ichrem(self,*args):
        return GiacMethods['ichrem'](self,*args)

     def icontent(self,*args):
        return GiacMethods['icontent'](self,*args)

     def icosahedron(self,*args):
        return GiacMethods['icosahedron'](self,*args)

     def id(self,*args):
        return GiacMethods['id'](self,*args)

     def identity(self,*args):
        return GiacMethods['identity'](self,*args)

     def idivis(self,*args):
        return GiacMethods['idivis'](self,*args)

     def idn(self,*args):
        return GiacMethods['idn'](self,*args)

     def iegcd(self,*args):
        return GiacMethods['iegcd'](self,*args)

     def ifactor(self,*args):
        return GiacMethods['ifactor'](self,*args)

     def ifactors(self,*args):
        return GiacMethods['ifactors'](self,*args)

     def igamma(self,*args):
        return GiacMethods['igamma'](self,*args)

     def igcd(self,*args):
        return GiacMethods['igcd'](self,*args)

     def igcdex(self,*args):
        return GiacMethods['igcdex'](self,*args)

     def ihermite(self,*args):
        return GiacMethods['ihermite'](self,*args)

     def ilaplace(self,*args):
        return GiacMethods['ilaplace'](self,*args)

     def im(self,*args):
        return GiacMethods['im'](self,*args)

     def imag(self,*args):
        return GiacMethods['imag'](self,*args)

     def image(self,*args):
        return GiacMethods['image'](self,*args)

     def implicitplot(self,*args):
        return GiacMethods['implicitplot'](self,*args)

     def inString(self,*args):
        return GiacMethods['inString'](self,*args)

     def in_ideal(self,*args):
        return GiacMethods['in_ideal'](self,*args)

     def incircle(self,*args):
        return GiacMethods['incircle'](self,*args)

     def indets(self,*args):
        return GiacMethods['indets'](self,*args)

     def inequationplot(self,*args):
        return GiacMethods['inequationplot'](self,*args)

     def inf(self,*args):
        return GiacMethods['inf'](self,*args)

     def infinity(self,*args):
        return GiacMethods['infinity'](self,*args)

     def infnorm(self,*args):
        return GiacMethods['infnorm'](self,*args)

     def insert(self,*args):
        return GiacMethods['insert'](self,*args)

     def insmod(self,*args):
        return GiacMethods['insmod'](self,*args)

     def int(self,*args):
        return GiacMethods['int'](self,*args)

     def intDiv(self,*args):
        return GiacMethods['intDiv'](self,*args)

     def integer(self,*args):
        return GiacMethods['integer'](self,*args)

     def integrate(self,*args):
        return GiacMethods['integrate'](self,*args)

     def integrer(self,*args):
        return GiacMethods['integrer'](self,*args)

     def inter(self,*args):
        return GiacMethods['inter'](self,*args)

     def interactive_odeplot(self,*args):
        return GiacMethods['interactive_odeplot'](self,*args)

     def interactive_plotode(self,*args):
        return GiacMethods['interactive_plotode'](self,*args)

     def interp(self,*args):
        return GiacMethods['interp'](self,*args)

     def interval(self,*args):
        return GiacMethods['interval'](self,*args)

     def interval2center(self,*args):
        return GiacMethods['interval2center'](self,*args)

     def inv(self,*args):
        return GiacMethods['inv'](self,*args)

     def inverse(self,*args):
        return GiacMethods['inverse'](self,*args)

     def inversion(self,*args):
        return GiacMethods['inversion'](self,*args)

     def invisible_point(self,*args):
        return GiacMethods['invisible_point'](self,*args)

     def invlaplace(self,*args):
        return GiacMethods['invlaplace'](self,*args)

     def invztrans(self,*args):
        return GiacMethods['invztrans'](self,*args)

     def iquo(self,*args):
        return GiacMethods['iquo'](self,*args)

     def iquorem(self,*args):
        return GiacMethods['iquorem'](self,*args)

     def iratrecon(self,*args):
        return GiacMethods['iratrecon'](self,*args)

     def irem(self,*args):
        return GiacMethods['irem'](self,*args)

     def isPrime(self,*args):
        return GiacMethods['isPrime'](self,*args)

     def is_collinear(self,*args):
        return GiacMethods['is_collinear'](self,*args)

     def is_concyclic(self,*args):
        return GiacMethods['is_concyclic'](self,*args)

     def is_conjugate(self,*args):
        return GiacMethods['is_conjugate'](self,*args)

     def is_coplanar(self,*args):
        return GiacMethods['is_coplanar'](self,*args)

     def is_cospheric(self,*args):
        return GiacMethods['is_cospheric'](self,*args)

     def is_cycle(self,*args):
        return GiacMethods['is_cycle'](self,*args)

     def is_element(self,*args):
        return GiacMethods['is_element'](self,*args)

     def is_equilateral(self,*args):
        return GiacMethods['is_equilateral'](self,*args)

     def is_harmonic(self,*args):
        return GiacMethods['is_harmonic'](self,*args)

     def is_harmonic_circle_bundle(self,*args):
        return GiacMethods['is_harmonic_circle_bundle'](self,*args)

     def is_harmonic_line_bundle(self,*args):
        return GiacMethods['is_harmonic_line_bundle'](self,*args)

     def is_inside(self,*args):
        return GiacMethods['is_inside'](self,*args)

     def is_isosceles(self,*args):
        return GiacMethods['is_isosceles'](self,*args)

     def is_orthogonal(self,*args):
        return GiacMethods['is_orthogonal'](self,*args)

     def is_parallel(self,*args):
        return GiacMethods['is_parallel'](self,*args)

     def is_parallelogram(self,*args):
        return GiacMethods['is_parallelogram'](self,*args)

     def is_permu(self,*args):
        return GiacMethods['is_permu'](self,*args)

     def is_perpendicular(self,*args):
        return GiacMethods['is_perpendicular'](self,*args)

     def is_prime(self,*args):
        return GiacMethods['is_prime'](self,*args)

     def is_pseudoprime(self,*args):
        return GiacMethods['is_pseudoprime'](self,*args)

     def is_rectangle(self,*args):
        return GiacMethods['is_rectangle'](self,*args)

     def is_rhombus(self,*args):
        return GiacMethods['is_rhombus'](self,*args)

     def is_square(self,*args):
        return GiacMethods['is_square'](self,*args)

     def ismith(self,*args):
        return GiacMethods['ismith'](self,*args)

     def isobarycenter(self,*args):
        return GiacMethods['isobarycenter'](self,*args)

     def isom(self,*args):
        return GiacMethods['isom'](self,*args)

     def isopolygon(self,*args):
        return GiacMethods['isopolygon'](self,*args)

     def isosceles_triangle(self,*args):
        return GiacMethods['isosceles_triangle'](self,*args)

     def isprime(self,*args):
        return GiacMethods['isprime'](self,*args)

     def ithprime(self,*args):
        return GiacMethods['ithprime'](self,*args)

     def jacobi_linsolve(self,*args):
        return GiacMethods['jacobi_linsolve'](self,*args)

     def jacobi_symbol(self,*args):
        return GiacMethods['jacobi_symbol'](self,*args)

     def jordan(self,*args):
        return GiacMethods['jordan'](self,*args)

     def keep_pivot(self,*args):
        return GiacMethods['keep_pivot'](self,*args)

     def ker(self,*args):
        return GiacMethods['ker'](self,*args)

     def kernel(self,*args):
        return GiacMethods['kernel'](self,*args)

     def kolmogorovd(self,*args):
        return GiacMethods['kolmogorovd'](self,*args)

     def kolmogorovt(self,*args):
        return GiacMethods['kolmogorovt'](self,*args)

     def l1norm(self,*args):
        return GiacMethods['l1norm'](self,*args)

     def l2norm(self,*args):
        return GiacMethods['l2norm'](self,*args)

     def lagrange(self,*args):
        return GiacMethods['lagrange'](self,*args)

     def laguerre(self,*args):
        return GiacMethods['laguerre'](self,*args)

     def laplace(self,*args):
        return GiacMethods['laplace'](self,*args)

     def laplacian(self,*args):
        return GiacMethods['laplacian'](self,*args)

     def latex(self,*args):
        return GiacMethods['latex'](self,*args)

     def lcm(self,*args):
        return GiacMethods['lcm'](self,*args)

     def lcoeff(self,*args):
        return GiacMethods['lcoeff'](self,*args)

     def ldegree(self,*args):
        return GiacMethods['ldegree'](self,*args)

     def left(self,*args):
        return GiacMethods['left'](self,*args)

     def left_rectangle(self,*args):
        return GiacMethods['left_rectangle'](self,*args)

     def legend(self,*args):
        return GiacMethods['legend'](self,*args)

     def legendre(self,*args):
        return GiacMethods['legendre'](self,*args)

     def legendre_symbol(self,*args):
        return GiacMethods['legendre_symbol'](self,*args)

     def length(self,*args):
        return GiacMethods['length'](self,*args)

     def lgcd(self,*args):
        return GiacMethods['lgcd'](self,*args)

     def lhs(self,*args):
        return GiacMethods['lhs'](self,*args)

     def ligne_chapeau_carre(self,*args):
        return GiacMethods['ligne_chapeau_carre'](self,*args)

     def ligne_chapeau_plat(self,*args):
        return GiacMethods['ligne_chapeau_plat'](self,*args)

     def ligne_chapeau_rond(self,*args):
        return GiacMethods['ligne_chapeau_rond'](self,*args)

     def ligne_polygonale(self,*args):
        return GiacMethods['ligne_polygonale'](self,*args)

     def ligne_polygonale_pointee(self,*args):
        return GiacMethods['ligne_polygonale_pointee'](self,*args)

     def ligne_tiret(self,*args):
        return GiacMethods['ligne_tiret'](self,*args)

     def ligne_tiret_point(self,*args):
        return GiacMethods['ligne_tiret_point'](self,*args)

     def ligne_tiret_pointpoint(self,*args):
        return GiacMethods['ligne_tiret_pointpoint'](self,*args)

     def ligne_trait_plein(self,*args):
        return GiacMethods['ligne_trait_plein'](self,*args)

     def limit(self,*args):
        return GiacMethods['limit'](self,*args)

     def limite(self,*args):
        return GiacMethods['limite'](self,*args)

     def lin(self,*args):
        return GiacMethods['lin'](self,*args)

     def line(self,*args):
        return GiacMethods['line'](self,*args)

     def line_inter(self,*args):
        return GiacMethods['line_inter'](self,*args)

     def line_paper(self,*args):
        return GiacMethods['line_paper'](self,*args)

     def line_segments(self,*args):
        return GiacMethods['line_segments'](self,*args)

     def linear_interpolate(self,*args):
        return GiacMethods['linear_interpolate'](self,*args)

     def linear_regression(self,*args):
        return GiacMethods['linear_regression'](self,*args)

     def linear_regression_plot(self,*args):
        return GiacMethods['linear_regression_plot'](self,*args)

     def lineariser(self,*args):
        return GiacMethods['lineariser'](self,*args)

     def lineariser_trigo(self,*args):
        return GiacMethods['lineariser_trigo'](self,*args)

     def linsolve(self,*args):
        return GiacMethods['linsolve'](self,*args)

     def linspace(self,*args):
        return GiacMethods['linspace'](self,*args)

     def lis_phrase(self,*args):
        return GiacMethods['lis_phrase'](self,*args)

     def list2mat(self,*args):
        return GiacMethods['list2mat'](self,*args)

     def listplot(self,*args):
        return GiacMethods['listplot'](self,*args)

     def lll(self,*args):
        return GiacMethods['lll'](self,*args)

     def ln(self,*args):
        return GiacMethods['ln'](self,*args)

     def lname(self,*args):
        return GiacMethods['lname'](self,*args)

     def lncollect(self,*args):
        return GiacMethods['lncollect'](self,*args)

     def lnexpand(self,*args):
        return GiacMethods['lnexpand'](self,*args)

     def locus(self,*args):
        return GiacMethods['locus'](self,*args)

     def log(self,*args):
        return GiacMethods['log'](self,*args)

     def log10(self,*args):
        return GiacMethods['log10'](self,*args)

     def logarithmic_regression(self,*args):
        return GiacMethods['logarithmic_regression'](self,*args)

     def logarithmic_regression_plot(self,*args):
        return GiacMethods['logarithmic_regression_plot'](self,*args)

     def logb(self,*args):
        return GiacMethods['logb'](self,*args)

     def logistic_regression(self,*args):
        return GiacMethods['logistic_regression'](self,*args)

     def logistic_regression_plot(self,*args):
        return GiacMethods['logistic_regression_plot'](self,*args)

     def lpsolve(self,*args):
        return GiacMethods['lpsolve'](self,*args)

     def lsmod(self,*args):
        return GiacMethods['lsmod'](self,*args)

     def lsq(self,*args):
        return GiacMethods['lsq'](self,*args)

     def lu(self,*args):
        return GiacMethods['lu'](self,*args)

     def lvar(self,*args):
        return GiacMethods['lvar'](self,*args)

     def mRow(self,*args):
        return GiacMethods['mRow'](self,*args)

     def mRowAdd(self,*args):
        return GiacMethods['mRowAdd'](self,*args)

     def magenta(self,*args):
        return GiacMethods['magenta'](self,*args)

     def makelist(self,*args):
        return GiacMethods['makelist'](self,*args)

     def makemat(self,*args):
        return GiacMethods['makemat'](self,*args)

     def makesuite(self,*args):
        return GiacMethods['makesuite'](self,*args)

     def makevector(self,*args):
        return GiacMethods['makevector'](self,*args)

     def map(self,*args):
        return GiacMethods['map'](self,*args)

     def maple2mupad(self,*args):
        return GiacMethods['maple2mupad'](self,*args)

     def maple2xcas(self,*args):
        return GiacMethods['maple2xcas'](self,*args)

     def maple_ifactors(self,*args):
        return GiacMethods['maple_ifactors'](self,*args)

     def maple_mode(self,*args):
        return GiacMethods['maple_mode'](self,*args)

     def markov(self,*args):
        return GiacMethods['markov'](self,*args)

     def mat2list(self,*args):
        return GiacMethods['mat2list'](self,*args)

     def mathml(self,*args):
        return GiacMethods['mathml'](self,*args)

     def matpow(self,*args):
        return GiacMethods['matpow'](self,*args)

     def matrix(self,*args):
        return GiacMethods['matrix'](self,*args)

     def matrix_norm(self,*args):
        return GiacMethods['matrix_norm'](self,*args)

     def max(self,*args):
        return GiacMethods['max'](self,*args)

     def maximize(self,*args):
        return GiacMethods['maximize'](self,*args)

     def maxnorm(self,*args):
        return GiacMethods['maxnorm'](self,*args)

     def mean(self,*args):
        return GiacMethods['mean'](self,*args)

     def median(self,*args):
        return GiacMethods['median'](self,*args)

     def median_line(self,*args):
        return GiacMethods['median_line'](self,*args)

     def member(self,*args):
        return GiacMethods['member'](self,*args)

     def mgf(self,*args):
        return GiacMethods['mgf'](self,*args)

     def mid(self,*args):
        return GiacMethods['mid'](self,*args)

     def middle_point(self,*args):
        return GiacMethods['middle_point'](self,*args)

     def midpoint(self,*args):
        return GiacMethods['midpoint'](self,*args)

     def min(self,*args):
        return GiacMethods['min'](self,*args)

     def minimax(self,*args):
        return GiacMethods['minimax'](self,*args)

     def minimize(self,*args):
        return GiacMethods['minimize'](self,*args)

     def mkisom(self,*args):
        return GiacMethods['mkisom'](self,*args)

     def mksa(self,*args):
        return GiacMethods['mksa'](self,*args)

     def modgcd(self,*args):
        return GiacMethods['modgcd'](self,*args)

     def mods(self,*args):
        return GiacMethods['mods'](self,*args)

     def montre_tortue(self,*args):
        return GiacMethods['montre_tortue'](self,*args)

     def moustache(self,*args):
        return GiacMethods['moustache'](self,*args)

     def moyal(self,*args):
        return GiacMethods['moyal'](self,*args)

     def moyenne(self,*args):
        return GiacMethods['moyenne'](self,*args)

     def mul(self,*args):
        return GiacMethods['mul'](self,*args)

     def mult_c_conjugate(self,*args):
        return GiacMethods['mult_c_conjugate'](self,*args)

     def mult_conjugate(self,*args):
        return GiacMethods['mult_conjugate'](self,*args)

     def multinomial(self,*args):
        return GiacMethods['multinomial'](self,*args)

     def multiplier_conjugue(self,*args):
        return GiacMethods['multiplier_conjugue'](self,*args)

     def multiplier_conjugue_complexe(self,*args):
        return GiacMethods['multiplier_conjugue_complexe'](self,*args)

     def multiply(self,*args):
        return GiacMethods['multiply'](self,*args)

     def mupad2maple(self,*args):
        return GiacMethods['mupad2maple'](self,*args)

     def mupad2xcas(self,*args):
        return GiacMethods['mupad2xcas'](self,*args)

     def nCr(self,*args):
        return GiacMethods['nCr'](self,*args)

     def nDeriv(self,*args):
        return GiacMethods['nDeriv'](self,*args)

     def nInt(self,*args):
        return GiacMethods['nInt'](self,*args)

     def nPr(self,*args):
        return GiacMethods['nPr'](self,*args)

     def nSolve(self,*args):
        return GiacMethods['nSolve'](self,*args)

     def ncols(self,*args):
        return GiacMethods['ncols'](self,*args)

     def negbinomial(self,*args):
        return GiacMethods['negbinomial'](self,*args)

     def negbinomial_cdf(self,*args):
        return GiacMethods['negbinomial_cdf'](self,*args)

     def negbinomial_icdf(self,*args):
        return GiacMethods['negbinomial_icdf'](self,*args)

     def newList(self,*args):
        return GiacMethods['newList'](self,*args)

     def newMat(self,*args):
        return GiacMethods['newMat'](self,*args)

     def newton(self,*args):
        return GiacMethods['newton'](self,*args)

     def newton_solver(self,*args):
        return GiacMethods['newton_solver'](self,*args)

     def newtonj_solver(self,*args):
        return GiacMethods['newtonj_solver'](self,*args)

     def nextperm(self,*args):
        return GiacMethods['nextperm'](self,*args)

     def nextprime(self,*args):
        return GiacMethods['nextprime'](self,*args)

     def nodisp(self,*args):
        return GiacMethods['nodisp'](self,*args)

     def non_recursive_normal(self,*args):
        return GiacMethods['non_recursive_normal'](self,*args)

     def nop(self,*args):
        return GiacMethods['nop'](self,*args)

     def nops(self,*args):
        return GiacMethods['nops'](self,*args)

     def norm(self,*args):
        return GiacMethods['norm'](self,*args)

     def normal(self,*args):
        return GiacMethods['normal'](self,*args)

     def normal_cdf(self,*args):
        return GiacMethods['normal_cdf'](self,*args)

     def normal_icdf(self,*args):
        return GiacMethods['normal_icdf'](self,*args)

     def normald(self,*args):
        return GiacMethods['normald'](self,*args)

     def normald_cdf(self,*args):
        return GiacMethods['normald_cdf'](self,*args)

     def normald_icdf(self,*args):
        return GiacMethods['normald_icdf'](self,*args)

     def normalize(self,*args):
        return GiacMethods['normalize'](self,*args)

     def normalt(self,*args):
        return GiacMethods['normalt'](self,*args)

     def nprimes(self,*args):
        return GiacMethods['nprimes'](self,*args)

     def nrows(self,*args):
        return GiacMethods['nrows'](self,*args)

     def nuage_points(self,*args):
        return GiacMethods['nuage_points'](self,*args)

     def nullspace(self,*args):
        return GiacMethods['nullspace'](self,*args)

     def numer(self,*args):
        return GiacMethods['numer'](self,*args)

     def octahedron(self,*args):
        return GiacMethods['octahedron'](self,*args)

     def odd(self,*args):
        return GiacMethods['odd'](self,*args)

     def odeplot(self,*args):
        return GiacMethods['odeplot'](self,*args)

     def odesolve(self,*args):
        return GiacMethods['odesolve'](self,*args)

     def op(self,*args):
        return GiacMethods['op'](self,*args)

     def open_polygon(self,*args):
        return GiacMethods['open_polygon'](self,*args)

     def ord(self,*args):
        return GiacMethods['ord'](self,*args)

     def order_size(self,*args):
        return GiacMethods['order_size'](self,*args)

     def ordinate(self,*args):
        return GiacMethods['ordinate'](self,*args)

     def orthocenter(self,*args):
        return GiacMethods['orthocenter'](self,*args)

     def orthogonal(self,*args):
        return GiacMethods['orthogonal'](self,*args)

     def osculating_circle(self,*args):
        return GiacMethods['osculating_circle'](self,*args)

     def p1oc2(self,*args):
        return GiacMethods['p1oc2'](self,*args)

     def p1op2(self,*args):
        return GiacMethods['p1op2'](self,*args)

     def pa2b2(self,*args):
        return GiacMethods['pa2b2'](self,*args)

     def pade(self,*args):
        return GiacMethods['pade'](self,*args)

     def parabola(self,*args):
        return GiacMethods['parabola'](self,*args)

     def parallel(self,*args):
        return GiacMethods['parallel'](self,*args)

     def parallelepiped(self,*args):
        return GiacMethods['parallelepiped'](self,*args)

     def parallelogram(self,*args):
        return GiacMethods['parallelogram'](self,*args)

     def parameq(self,*args):
        return GiacMethods['parameq'](self,*args)

     def parameter(self,*args):
        return GiacMethods['parameter'](self,*args)

     def paramplot(self,*args):
        return GiacMethods['paramplot'](self,*args)

     def parfrac(self,*args):
        return GiacMethods['parfrac'](self,*args)

     def pari(self,*args):
        return GiacMethods['pari'](self,*args)

     def part(self,*args):
        return GiacMethods['part'](self,*args)

     def partfrac(self,*args):
        return GiacMethods['partfrac'](self,*args)

     def pas_de_cote(self,*args):
        return GiacMethods['pas_de_cote'](self,*args)

     def pcar(self,*args):
        return GiacMethods['pcar'](self,*args)

     def pcar_hessenberg(self,*args):
        return GiacMethods['pcar_hessenberg'](self,*args)

     def pcoef(self,*args):
        return GiacMethods['pcoef'](self,*args)

     def pcoeff(self,*args):
        return GiacMethods['pcoeff'](self,*args)

     def perimeter(self,*args):
        return GiacMethods['perimeter'](self,*args)

     def perimeterat(self,*args):
        return GiacMethods['perimeterat'](self,*args)

     def perimeteratraw(self,*args):
        return GiacMethods['perimeteratraw'](self,*args)

     def perm(self,*args):
        return GiacMethods['perm'](self,*args)

     def perminv(self,*args):
        return GiacMethods['perminv'](self,*args)

     def permu2cycles(self,*args):
        return GiacMethods['permu2cycles'](self,*args)

     def permu2mat(self,*args):
        return GiacMethods['permu2mat'](self,*args)

     def permuorder(self,*args):
        return GiacMethods['permuorder'](self,*args)

     def perpen_bisector(self,*args):
        return GiacMethods['perpen_bisector'](self,*args)

     def perpendicular(self,*args):
        return GiacMethods['perpendicular'](self,*args)

     def peval(self,*args):
        return GiacMethods['peval'](self,*args)

     def pi(self,*args):
        return GiacMethods['pi'](self,*args)

     def piecewise(self,*args):
        return GiacMethods['piecewise'](self,*args)

     def pivot(self,*args):
        return GiacMethods['pivot'](self,*args)

     def pixoff(self,*args):
        return GiacMethods['pixoff'](self,*args)

     def pixon(self,*args):
        return GiacMethods['pixon'](self,*args)

     def plane(self,*args):
        return GiacMethods['plane'](self,*args)

     def playsnd(self,*args):
        return GiacMethods['playsnd'](self,*args)

     def plex(self,*args):
        return GiacMethods['plex'](self,*args)

     def plot(self,*args):
        return GiacMethods['plot'](self,*args)

     def plot3d(self,*args):
        return GiacMethods['plot3d'](self,*args)

     def plotarea(self,*args):
        return GiacMethods['plotarea'](self,*args)

     def plotcdf(self,*args):
        return GiacMethods['plotcdf'](self,*args)

     def plotcontour(self,*args):
        return GiacMethods['plotcontour'](self,*args)

     def plotdensity(self,*args):
        return GiacMethods['plotdensity'](self,*args)

     def plotfield(self,*args):
        return GiacMethods['plotfield'](self,*args)

     def plotfunc(self,*args):
        return GiacMethods['plotfunc'](self,*args)

     def plotimplicit(self,*args):
        return GiacMethods['plotimplicit'](self,*args)

     def plotinequation(self,*args):
        return GiacMethods['plotinequation'](self,*args)

     def plotlist(self,*args):
        return GiacMethods['plotlist'](self,*args)

     def plotode(self,*args):
        return GiacMethods['plotode'](self,*args)

     def plotparam(self,*args):
        return GiacMethods['plotparam'](self,*args)

     def plotpolar(self,*args):
        return GiacMethods['plotpolar'](self,*args)

     def plotseq(self,*args):
        return GiacMethods['plotseq'](self,*args)

     def plus_point(self,*args):
        return GiacMethods['plus_point'](self,*args)

     def pmin(self,*args):
        return GiacMethods['pmin'](self,*args)

     def point(self,*args):
        return GiacMethods['point'](self,*args)

     def point2d(self,*args):
        return GiacMethods['point2d'](self,*args)

     def point3d(self,*args):
        return GiacMethods['point3d'](self,*args)

     def poisson(self,*args):
        return GiacMethods['poisson'](self,*args)

     def poisson_cdf(self,*args):
        return GiacMethods['poisson_cdf'](self,*args)

     def poisson_icdf(self,*args):
        return GiacMethods['poisson_icdf'](self,*args)

     def polar(self,*args):
        return GiacMethods['polar'](self,*args)

     def polar_coordinates(self,*args):
        return GiacMethods['polar_coordinates'](self,*args)

     def polar_point(self,*args):
        return GiacMethods['polar_point'](self,*args)

     def polarplot(self,*args):
        return GiacMethods['polarplot'](self,*args)

     def pole(self,*args):
        return GiacMethods['pole'](self,*args)

     def poly2symb(self,*args):
        return GiacMethods['poly2symb'](self,*args)

     def polyEval(self,*args):
        return GiacMethods['polyEval'](self,*args)

     def polygon(self,*args):
        return GiacMethods['polygon'](self,*args)

     def polygone_rempli(self,*args):
        return GiacMethods['polygone_rempli'](self,*args)

     def polygonplot(self,*args):
        return GiacMethods['polygonplot'](self,*args)

     def polygonscatterplot(self,*args):
        return GiacMethods['polygonscatterplot'](self,*args)

     def polyhedron(self,*args):
        return GiacMethods['polyhedron'](self,*args)

     def polynom(self,*args):
        return GiacMethods['polynom'](self,*args)

     def polynomial_regression(self,*args):
        return GiacMethods['polynomial_regression'](self,*args)

     def polynomial_regression_plot(self,*args):
        return GiacMethods['polynomial_regression_plot'](self,*args)

     def position(self,*args):
        return GiacMethods['position'](self,*args)

     def poslbdLMQ(self,*args):
        return GiacMethods['poslbdLMQ'](self,*args)

     def posubLMQ(self,*args):
        return GiacMethods['posubLMQ'](self,*args)

     def potential(self,*args):
        return GiacMethods['potential'](self,*args)

     def pow2exp(self,*args):
        return GiacMethods['pow2exp'](self,*args)

     def power_regression(self,*args):
        return GiacMethods['power_regression'](self,*args)

     def power_regression_plot(self,*args):
        return GiacMethods['power_regression_plot'](self,*args)

     def powermod(self,*args):
        return GiacMethods['powermod'](self,*args)

     def powerpc(self,*args):
        return GiacMethods['powerpc'](self,*args)

     def powexpand(self,*args):
        return GiacMethods['powexpand'](self,*args)

     def powmod(self,*args):
        return GiacMethods['powmod'](self,*args)

     def prepend(self,*args):
        return GiacMethods['prepend'](self,*args)

     def preval(self,*args):
        return GiacMethods['preval'](self,*args)

     def prevperm(self,*args):
        return GiacMethods['prevperm'](self,*args)

     def prevprime(self,*args):
        return GiacMethods['prevprime'](self,*args)

     def primpart(self,*args):
        return GiacMethods['primpart'](self,*args)

     def prism(self,*args):
        return GiacMethods['prism'](self,*args)

     def product(self,*args):
        return GiacMethods['product'](self,*args)

     def projection(self,*args):
        return GiacMethods['projection'](self,*args)

     def proot(self,*args):
        return GiacMethods['proot'](self,*args)

     def propFrac(self,*args):
        return GiacMethods['propFrac'](self,*args)

     def propfrac(self,*args):
        return GiacMethods['propfrac'](self,*args)

     def psrgcd(self,*args):
        return GiacMethods['psrgcd'](self,*args)

     def ptayl(self,*args):
        return GiacMethods['ptayl'](self,*args)

     def purge(self,*args):
        return GiacMethods['purge'](self,*args)

     def pwd(self,*args):
        return GiacMethods['pwd'](self,*args)

     def pyramid(self,*args):
        return GiacMethods['pyramid'](self,*args)

     def q2a(self,*args):
        return GiacMethods['q2a'](self,*args)

     def qr(self,*args):
        return GiacMethods['qr'](self,*args)

     def quadric(self,*args):
        return GiacMethods['quadric'](self,*args)

     def quadrilateral(self,*args):
        return GiacMethods['quadrilateral'](self,*args)

     def quantile(self,*args):
        return GiacMethods['quantile'](self,*args)

     def quartile1(self,*args):
        return GiacMethods['quartile1'](self,*args)

     def quartile3(self,*args):
        return GiacMethods['quartile3'](self,*args)

     def quartiles(self,*args):
        return GiacMethods['quartiles'](self,*args)

     def quest(self,*args):
        return GiacMethods['quest'](self,*args)

     def quo(self,*args):
        return GiacMethods['quo'](self,*args)

     def quorem(self,*args):
        return GiacMethods['quorem'](self,*args)

     def quote(self,*args):
        return GiacMethods['quote'](self,*args)

     def r2e(self,*args):
        return GiacMethods['r2e'](self,*args)

     def radical_axis(self,*args):
        return GiacMethods['radical_axis'](self,*args)

     def radius(self,*args):
        return GiacMethods['radius'](self,*args)

     def ramene(self,*args):
        return GiacMethods['ramene'](self,*args)

     def rand(self,*args):
        return GiacMethods['rand'](self,*args)

     def randMat(self,*args):
        return GiacMethods['randMat'](self,*args)

     def randNorm(self,*args):
        return GiacMethods['randNorm'](self,*args)

     def randPoly(self,*args):
        return GiacMethods['randPoly'](self,*args)

     def randbinomial(self,*args):
        return GiacMethods['randbinomial'](self,*args)

     def randchisquare(self,*args):
        return GiacMethods['randchisquare'](self,*args)

     def randexp(self,*args):
        return GiacMethods['randexp'](self,*args)

     def randfisher(self,*args):
        return GiacMethods['randfisher'](self,*args)

     def randgeometric(self,*args):
        return GiacMethods['randgeometric'](self,*args)

     def randmarkov(self,*args):
        return GiacMethods['randmarkov'](self,*args)

     def randmatrix(self,*args):
        return GiacMethods['randmatrix'](self,*args)

     def randmultinomial(self,*args):
        return GiacMethods['randmultinomial'](self,*args)

     def randnorm(self,*args):
        return GiacMethods['randnorm'](self,*args)

     def randperm(self,*args):
        return GiacMethods['randperm'](self,*args)

     def randpoisson(self,*args):
        return GiacMethods['randpoisson'](self,*args)

     def randpoly(self,*args):
        return GiacMethods['randpoly'](self,*args)

     def randseed(self,*args):
        return GiacMethods['randseed'](self,*args)

     def randstudent(self,*args):
        return GiacMethods['randstudent'](self,*args)

     def randvector(self,*args):
        return GiacMethods['randvector'](self,*args)

     def rank(self,*args):
        return GiacMethods['rank'](self,*args)

     def ranm(self,*args):
        return GiacMethods['ranm'](self,*args)

     def ranv(self,*args):
        return GiacMethods['ranv'](self,*args)

     def rassembler_trigo(self,*args):
        return GiacMethods['rassembler_trigo'](self,*args)

     def rat_jordan(self,*args):
        return GiacMethods['rat_jordan'](self,*args)

     def rational(self,*args):
        return GiacMethods['rational'](self,*args)

     def rationalroot(self,*args):
        return GiacMethods['rationalroot'](self,*args)

     def ratnormal(self,*args):
        return GiacMethods['ratnormal'](self,*args)

     def rcl(self,*args):
        return GiacMethods['rcl'](self,*args)

     def rdiv(self,*args):
        return GiacMethods['rdiv'](self,*args)

     def re(self,*args):
        return GiacMethods['re'](self,*args)

     def read(self,*args):
        return GiacMethods['read'](self,*args)

     def readrgb(self,*args):
        return GiacMethods['readrgb'](self,*args)

     def readwav(self,*args):
        return GiacMethods['readwav'](self,*args)

     def real(self,*args):
        return GiacMethods['real'](self,*args)

     def realroot(self,*args):
        return GiacMethods['realroot'](self,*args)

     def reciprocation(self,*args):
        return GiacMethods['reciprocation'](self,*args)

     def rectangle(self,*args):
        return GiacMethods['rectangle'](self,*args)

     def rectangle_droit(self,*args):
        return GiacMethods['rectangle_droit'](self,*args)

     def rectangle_gauche(self,*args):
        return GiacMethods['rectangle_gauche'](self,*args)

     def rectangle_plein(self,*args):
        return GiacMethods['rectangle_plein'](self,*args)

     def rectangular_coordinates(self,*args):
        return GiacMethods['rectangular_coordinates'](self,*args)

     def recule(self,*args):
        return GiacMethods['recule'](self,*args)

     def red(self,*args):
        return GiacMethods['red'](self,*args)

     def reduced_conic(self,*args):
        return GiacMethods['reduced_conic'](self,*args)

     def reduced_quadric(self,*args):
        return GiacMethods['reduced_quadric'](self,*args)

     def ref(self,*args):
        return GiacMethods['ref'](self,*args)

     def reflection(self,*args):
        return GiacMethods['reflection'](self,*args)

     def regroup(self,*args):
        return GiacMethods['regroup'](self,*args)

     def rem(self,*args):
        return GiacMethods['rem'](self,*args)

     def remain(self,*args):
        return GiacMethods['remain'](self,*args)

     def remove(self,*args):
        return GiacMethods['remove'](self,*args)

     def reorder(self,*args):
        return GiacMethods['reorder'](self,*args)

     def residue(self,*args):
        return GiacMethods['residue'](self,*args)

     def resoudre(self,*args):
        return GiacMethods['resoudre'](self,*args)

     def resoudre_dans_C(self,*args):
        return GiacMethods['resoudre_dans_C'](self,*args)

     def resoudre_systeme_lineaire(self,*args):
        return GiacMethods['resoudre_systeme_lineaire'](self,*args)

     def resultant(self,*args):
        return GiacMethods['resultant'](self,*args)

     def reverse(self,*args):
        return GiacMethods['reverse'](self,*args)

     def reverse_rsolve(self,*args):
        return GiacMethods['reverse_rsolve'](self,*args)

     def revert(self,*args):
        return GiacMethods['revert'](self,*args)

     def revlex(self,*args):
        return GiacMethods['revlex'](self,*args)

     def revlist(self,*args):
        return GiacMethods['revlist'](self,*args)

     def rhombus(self,*args):
        return GiacMethods['rhombus'](self,*args)

     def rhombus_point(self,*args):
        return GiacMethods['rhombus_point'](self,*args)

     def rhs(self,*args):
        return GiacMethods['rhs'](self,*args)

     def right(self,*args):
        return GiacMethods['right'](self,*args)

     def right_rectangle(self,*args):
        return GiacMethods['right_rectangle'](self,*args)

     def right_triangle(self,*args):
        return GiacMethods['right_triangle'](self,*args)

     def risch(self,*args):
        return GiacMethods['risch'](self,*args)

     def rm_a_z(self,*args):
        return GiacMethods['rm_a_z'](self,*args)

     def rm_all_vars(self,*args):
        return GiacMethods['rm_all_vars'](self,*args)

     def rmbreakpoint(self,*args):
        return GiacMethods['rmbreakpoint'](self,*args)

     def rmmod(self,*args):
        return GiacMethods['rmmod'](self,*args)

     def rmwatch(self,*args):
        return GiacMethods['rmwatch'](self,*args)

     def romberg(self,*args):
        return GiacMethods['romberg'](self,*args)

     def rombergm(self,*args):
        return GiacMethods['rombergm'](self,*args)

     def rombergt(self,*args):
        return GiacMethods['rombergt'](self,*args)

     def rond(self,*args):
        return GiacMethods['rond'](self,*args)

     def root(self,*args):
        return GiacMethods['root'](self,*args)

     def rootof(self,*args):
        return GiacMethods['rootof'](self,*args)

     def roots(self,*args):
        return GiacMethods['roots'](self,*args)

     def rotate(self,*args):
        return GiacMethods['rotate'](self,*args)

     def rotation(self,*args):
        return GiacMethods['rotation'](self,*args)

     def round(self,*args):
        return GiacMethods['round'](self,*args)

     def row(self,*args):
        return GiacMethods['row'](self,*args)

     def rowAdd(self,*args):
        return GiacMethods['rowAdd'](self,*args)

     def rowDim(self,*args):
        return GiacMethods['rowDim'](self,*args)

     def rowNorm(self,*args):
        return GiacMethods['rowNorm'](self,*args)

     def rowSwap(self,*args):
        return GiacMethods['rowSwap'](self,*args)

     def rowdim(self,*args):
        return GiacMethods['rowdim'](self,*args)

     def rownorm(self,*args):
        return GiacMethods['rownorm'](self,*args)

     def rowspace(self,*args):
        return GiacMethods['rowspace'](self,*args)

     def rowswap(self,*args):
        return GiacMethods['rowswap'](self,*args)

     def rref(self,*args):
        return GiacMethods['rref'](self,*args)

     def rsolve(self,*args):
        return GiacMethods['rsolve'](self,*args)

     def same(self,*args):
        return GiacMethods['same'](self,*args)

     def sans_factoriser(self,*args):
        return GiacMethods['sans_factoriser'](self,*args)

     def saute(self,*args):
        return GiacMethods['saute'](self,*args)

     def scalarProduct(self,*args):
        return GiacMethods['scalarProduct'](self,*args)

     def scalar_product(self,*args):
        return GiacMethods['scalar_product'](self,*args)

     def scatterplot(self,*args):
        return GiacMethods['scatterplot'](self,*args)

     def schur(self,*args):
        return GiacMethods['schur'](self,*args)

     def sec(self,*args):
        return GiacMethods['sec'](self,*args)

     def secant_solver(self,*args):
        return GiacMethods['secant_solver'](self,*args)

     def segment(self,*args):
        return GiacMethods['segment'](self,*args)

     def select(self,*args):
        return GiacMethods['select'](self,*args)

     def semi_augment(self,*args):
        return GiacMethods['semi_augment'](self,*args)

     def seq(self,*args):
        return GiacMethods['seq'](self,*args)

     def seqplot(self,*args):
        return GiacMethods['seqplot'](self,*args)

     def seqsolve(self,*args):
        return GiacMethods['seqsolve'](self,*args)

     def series(self,*args):
        return GiacMethods['series'](self,*args)

     def shift(self,*args):
        return GiacMethods['shift'](self,*args)

     def shift_phase(self,*args):
        return GiacMethods['shift_phase'](self,*args)

     def sign(self,*args):
        return GiacMethods['sign'](self,*args)

     def signature(self,*args):
        return GiacMethods['signature'](self,*args)

     def signe(self,*args):
        return GiacMethods['signe'](self,*args)

     def similarity(self,*args):
        return GiacMethods['similarity'](self,*args)

     def simp2(self,*args):
        return GiacMethods['simp2'](self,*args)

     def simplex_reduce(self,*args):
        return GiacMethods['simplex_reduce'](self,*args)

     def simplifier(self,*args):
        return GiacMethods['simplifier'](self,*args)

     def simplify(self,*args):
        return GiacMethods['simplify'](self,*args)

     def simpson(self,*args):
        return GiacMethods['simpson'](self,*args)

     def simult(self,*args):
        return GiacMethods['simult'](self,*args)

     def sin(self,*args):
        return GiacMethods['sin'](self,*args)

     def sin2costan(self,*args):
        return GiacMethods['sin2costan'](self,*args)

     def sincos(self,*args):
        return GiacMethods['sincos'](self,*args)

     def single_inter(self,*args):
        return GiacMethods['single_inter'](self,*args)

     def sinh(self,*args):
        return GiacMethods['sinh'](self,*args)

     def sizes(self,*args):
        return GiacMethods['sizes'](self,*args)

     def slope(self,*args):
        return GiacMethods['slope'](self,*args)

     def slopeat(self,*args):
        return GiacMethods['slopeat'](self,*args)

     def slopeatraw(self,*args):
        return GiacMethods['slopeatraw'](self,*args)

     def smith(self,*args):
        return GiacMethods['smith'](self,*args)

     def smod(self,*args):
        return GiacMethods['smod'](self,*args)

     def snedecor(self,*args):
        return GiacMethods['snedecor'](self,*args)

     def snedecor_cdf(self,*args):
        return GiacMethods['snedecor_cdf'](self,*args)

     def snedecor_icdf(self,*args):
        return GiacMethods['snedecor_icdf'](self,*args)

     def snedecord(self,*args):
        return GiacMethods['snedecord'](self,*args)

     def snedecord_cdf(self,*args):
        return GiacMethods['snedecord_cdf'](self,*args)

     def snedecord_icdf(self,*args):
        return GiacMethods['snedecord_icdf'](self,*args)

     def solid_line(self,*args):
        return GiacMethods['solid_line'](self,*args)

     def solve(self,*args):
        return GiacMethods['solve'](self,*args)

     def somme(self,*args):
        return GiacMethods['somme'](self,*args)

     def sommet(self,*args):
        return GiacMethods['sommet'](self,*args)

     def sort(self,*args):
        return GiacMethods['sort'](self,*args)

     def sorta(self,*args):
        return GiacMethods['sorta'](self,*args)

     def sortd(self,*args):
        return GiacMethods['sortd'](self,*args)

     def soundsec(self,*args):
        return GiacMethods['soundsec'](self,*args)

     def sphere(self,*args):
        return GiacMethods['sphere'](self,*args)

     def spline(self,*args):
        return GiacMethods['spline'](self,*args)

     def split(self,*args):
        return GiacMethods['split'](self,*args)

     def sq(self,*args):
        return GiacMethods['sq'](self,*args)

     def sqrfree(self,*args):
        return GiacMethods['sqrfree'](self,*args)

     def sqrt(self,*args):
        return GiacMethods['sqrt'](self,*args)

     def square(self,*args):
        return GiacMethods['square'](self,*args)

     def square_point(self,*args):
        return GiacMethods['square_point'](self,*args)

     def srand(self,*args):
        return GiacMethods['srand'](self,*args)

     def sst(self,*args):
        return GiacMethods['sst'](self,*args)

     def sst_in(self,*args):
        return GiacMethods['sst_in'](self,*args)

     def star_point(self,*args):
        return GiacMethods['star_point'](self,*args)

     def start(self,*args):
        return GiacMethods['start'](self,*args)

     def stdDev(self,*args):
        return GiacMethods['stdDev'](self,*args)

     def stddev(self,*args):
        return GiacMethods['stddev'](self,*args)

     def stddevp(self,*args):
        return GiacMethods['stddevp'](self,*args)

     def steffenson_solver(self,*args):
        return GiacMethods['steffenson_solver'](self,*args)

     def student(self,*args):
        return GiacMethods['student'](self,*args)

     def student_cdf(self,*args):
        return GiacMethods['student_cdf'](self,*args)

     def student_icdf(self,*args):
        return GiacMethods['student_icdf'](self,*args)

     def studentd(self,*args):
        return GiacMethods['studentd'](self,*args)

     def studentt(self,*args):
        return GiacMethods['studentt'](self,*args)

     def sturm(self,*args):
        return GiacMethods['sturm'](self,*args)

     def sturmab(self,*args):
        return GiacMethods['sturmab'](self,*args)

     def sturmseq(self,*args):
        return GiacMethods['sturmseq'](self,*args)

     def style(self,*args):
        return GiacMethods['style'](self,*args)

     def subMat(self,*args):
        return GiacMethods['subMat'](self,*args)

     def subs(self,*args):
        return GiacMethods['subs'](self,*args)

     def subsop(self,*args):
        return GiacMethods['subsop'](self,*args)

     def subst(self,*args):
        return GiacMethods['subst'](self,*args)

     def substituer(self,*args):
        return GiacMethods['substituer'](self,*args)

     def subtype(self,*args):
        return GiacMethods['subtype'](self,*args)

     def sum(self,*args):
        return GiacMethods['sum'](self,*args)

     def sum_riemann(self,*args):
        return GiacMethods['sum_riemann'](self,*args)

     def suppress(self,*args):
        return GiacMethods['suppress'](self,*args)

     def surd(self,*args):
        return GiacMethods['surd'](self,*args)

     def svd(self,*args):
        return GiacMethods['svd'](self,*args)

     def swapcol(self,*args):
        return GiacMethods['swapcol'](self,*args)

     def swaprow(self,*args):
        return GiacMethods['swaprow'](self,*args)

     def switch_axes(self,*args):
        return GiacMethods['switch_axes'](self,*args)

     def sylvester(self,*args):
        return GiacMethods['sylvester'](self,*args)

     def symb2poly(self,*args):
        return GiacMethods['symb2poly'](self,*args)

     def symbol(self,*args):
        return GiacMethods['symbol'](self,*args)

     def syst2mat(self,*args):
        return GiacMethods['syst2mat'](self,*args)

     def tCollect(self,*args):
        return GiacMethods['tCollect'](self,*args)

     def tExpand(self,*args):
        return GiacMethods['tExpand'](self,*args)

     def table(self,*args):
        return GiacMethods['table'](self,*args)

     def tablefunc(self,*args):
        return GiacMethods['tablefunc'](self,*args)

     def tableseq(self,*args):
        return GiacMethods['tableseq'](self,*args)

     def tabvar(self,*args):
        return GiacMethods['tabvar'](self,*args)

     def tail(self,*args):
        return GiacMethods['tail'](self,*args)

     def tan(self,*args):
        return GiacMethods['tan'](self,*args)

     def tan2cossin2(self,*args):
        return GiacMethods['tan2cossin2'](self,*args)

     def tan2sincos(self,*args):
        return GiacMethods['tan2sincos'](self,*args)

     def tan2sincos2(self,*args):
        return GiacMethods['tan2sincos2'](self,*args)

     def tangent(self,*args):
        return GiacMethods['tangent'](self,*args)

     def tangente(self,*args):
        return GiacMethods['tangente'](self,*args)

     def tanh(self,*args):
        return GiacMethods['tanh'](self,*args)

     def taux_accroissement(self,*args):
        return GiacMethods['taux_accroissement'](self,*args)

     def taylor(self,*args):
        return GiacMethods['taylor'](self,*args)

     def tchebyshev1(self,*args):
        return GiacMethods['tchebyshev1'](self,*args)

     def tchebyshev2(self,*args):
        return GiacMethods['tchebyshev2'](self,*args)

     def tcoeff(self,*args):
        return GiacMethods['tcoeff'](self,*args)

     def tcollect(self,*args):
        return GiacMethods['tcollect'](self,*args)

     def tdeg(self,*args):
        return GiacMethods['tdeg'](self,*args)

     def tetrahedron(self,*args):
        return GiacMethods['tetrahedron'](self,*args)

     def texpand(self,*args):
        return GiacMethods['texpand'](self,*args)

     def thickness(self,*args):
        return GiacMethods['thickness'](self,*args)

     def throw(self,*args):
        return GiacMethods['throw'](self,*args)

     def title(self,*args):
        return GiacMethods['title'](self,*args)

     def titre(self,*args):
        return GiacMethods['titre'](self,*args)

     def tlin(self,*args):
        return GiacMethods['tlin'](self,*args)

     def tourne_droite(self,*args):
        return GiacMethods['tourne_droite'](self,*args)

     def tourne_gauche(self,*args):
        return GiacMethods['tourne_gauche'](self,*args)

     def tpsolve(self,*args):
        return GiacMethods['tpsolve'](self,*args)

     def trace(self,*args):
        return GiacMethods['trace'](self,*args)

     def trames(self,*args):
        return GiacMethods['trames'](self,*args)

     def tran(self,*args):
        return GiacMethods['tran'](self,*args)

     def translation(self,*args):
        return GiacMethods['translation'](self,*args)

     def transpose(self,*args):
        return GiacMethods['transpose'](self,*args)

     def trapeze(self,*args):
        return GiacMethods['trapeze'](self,*args)

     def trapezoid(self,*args):
        return GiacMethods['trapezoid'](self,*args)

     def triangle(self,*args):
        return GiacMethods['triangle'](self,*args)

     def triangle_paper(self,*args):
        return GiacMethods['triangle_paper'](self,*args)

     def triangle_plein(self,*args):
        return GiacMethods['triangle_plein'](self,*args)

     def triangle_point(self,*args):
        return GiacMethods['triangle_point'](self,*args)

     def trig2exp(self,*args):
        return GiacMethods['trig2exp'](self,*args)

     def trigcos(self,*args):
        return GiacMethods['trigcos'](self,*args)

     def trigexpand(self,*args):
        return GiacMethods['trigexpand'](self,*args)

     def trigsin(self,*args):
        return GiacMethods['trigsin'](self,*args)

     def trigtan(self,*args):
        return GiacMethods['trigtan'](self,*args)

     def trn(self,*args):
        return GiacMethods['trn'](self,*args)

     def true(self,*args):
        return GiacMethods['true'](self,*args)

     def trunc(self,*args):
        return GiacMethods['trunc'](self,*args)

     def truncate(self,*args):
        return GiacMethods['truncate'](self,*args)

     def tsimplify(self,*args):
        return GiacMethods['tsimplify'](self,*args)

     def ufactor(self,*args):
        return GiacMethods['ufactor'](self,*args)

     def ugamma(self,*args):
        return GiacMethods['ugamma'](self,*args)

     def unapply(self,*args):
        return GiacMethods['unapply'](self,*args)

     def unarchive(self,*args):
        return GiacMethods['unarchive'](self,*args)

     def unfactored(self,*args):
        return GiacMethods['unfactored'](self,*args)

     def uniform(self,*args):
        return GiacMethods['uniform'](self,*args)

     def uniform_cdf(self,*args):
        return GiacMethods['uniform_cdf'](self,*args)

     def uniform_icdf(self,*args):
        return GiacMethods['uniform_icdf'](self,*args)

     def uniformd(self,*args):
        return GiacMethods['uniformd'](self,*args)

     def uniformd_cdf(self,*args):
        return GiacMethods['uniformd_cdf'](self,*args)

     def uniformd_icdf(self,*args):
        return GiacMethods['uniformd_icdf'](self,*args)

     def unitV(self,*args):
        return GiacMethods['unitV'](self,*args)

     def unquote(self,*args):
        return GiacMethods['unquote'](self,*args)

     def user_operator(self,*args):
        return GiacMethods['user_operator'](self,*args)

     def usimplify(self,*args):
        return GiacMethods['usimplify'](self,*args)

     def valuation(self,*args):
        return GiacMethods['valuation'](self,*args)

     def vandermonde(self,*args):
        return GiacMethods['vandermonde'](self,*args)

     def variables_are_files(self,*args):
        return GiacMethods['variables_are_files'](self,*args)

     def variance(self,*args):
        return GiacMethods['variance'](self,*args)

     def version(self,*args):
        return GiacMethods['version'](self,*args)

     def vertices(self,*args):
        return GiacMethods['vertices'](self,*args)

     def vertices_abc(self,*args):
        return GiacMethods['vertices_abc'](self,*args)

     def vertices_abca(self,*args):
        return GiacMethods['vertices_abca'](self,*args)

     def vpotential(self,*args):
        return GiacMethods['vpotential'](self,*args)

     def weibull(self,*args):
        return GiacMethods['weibull'](self,*args)

     def weibull_cdf(self,*args):
        return GiacMethods['weibull_cdf'](self,*args)

     def weibull_icdf(self,*args):
        return GiacMethods['weibull_icdf'](self,*args)

     def weibulld(self,*args):
        return GiacMethods['weibulld'](self,*args)

     def weibulld_cdf(self,*args):
        return GiacMethods['weibulld_cdf'](self,*args)

     def weibulld_icdf(self,*args):
        return GiacMethods['weibulld_icdf'](self,*args)

     def widget_size(self,*args):
        return GiacMethods['widget_size'](self,*args)

     def wilcoxonp(self,*args):
        return GiacMethods['wilcoxonp'](self,*args)

     def wilcoxons(self,*args):
        return GiacMethods['wilcoxons'](self,*args)

     def wilcoxont(self,*args):
        return GiacMethods['wilcoxont'](self,*args)

     def writergb(self,*args):
        return GiacMethods['writergb'](self,*args)

     def writewav(self,*args):
        return GiacMethods['writewav'](self,*args)

     def xyztrange(self,*args):
        return GiacMethods['xyztrange'](self,*args)

     def zeros(self,*args):
        return GiacMethods['zeros'](self,*args)

     def ztrans(self,*args):
        return GiacMethods['ztrans'](self,*args)

     def type(self,*args):
        return GiacMethods['type'](self,*args)

     def zip(self,*args):
        return GiacMethods['zip'](self,*args)





##
################################################################
#   A wrapper from a cpp element of type giac gen to create    #
#   the Python object                                          #
################################################################
cdef inline _wrap_gen(gen  g)except +:

#   cdef Pygen pyg=Pygen('NULL')
# It is much faster with ''
#      [x-x for i in range(10**4)]
#      ('clock: ', 0.010000000000000009,
# than with 'NULL':
#      [x-x for i in range(10**4)]
#      ('clock: ', 1.1999999999999997,
#    #    #    #    #    #
# This is faster than with:
#    cdef Pygen pyg=Pygen('')
# ll=giac(range(10**6))
# ('clock: ', 0.40000000000000036, ' time: ', 0.40346789360046387)
# gg=[1 for i in ll]
# ('clock: ', 0.669999999999999, ' time: ', 0.650738000869751)
#
# But beware when changing the None case in  Pygen init.
#
    cdef Pygen pyg=Pygen() # NB: for stability reasons it creates a full Pygen
    del pyg.gptr # so we have to free its gptr here to avoid a memory leak.
    pyg.gptr=new gen(g)
    return pyg
#    if(pyg.gptr !=NULL):
#      return pyg
#    else:
#      raise MemoryError,"empty gen"






################################################################
#    A wrapper from a python list to a vector of gen           #
################################################################

cdef  vecteur _wrap_pylist(L) except +:
   cdef Pygen pyg=Pygen()
   cdef vecteur  * V
   cdef int i

   if (isinstance(L,tuple) or isinstance(L,listrange)):
      n=len(L)
      V=new vecteur()
      ressetctrl_c()
#      sig_on()
      for i in range(n):
        if(GIACctrl_c):
          raise KeyboardInterrupt,"Interrupted by a ctrl-c event"
        V.push_back((<Pygen>Pygen(L[i])).gptr[0])
#      sig_off()
      return V[0]
   else:
     raise TypeError,"argument must be a tuple or a list"


#################################
#  slice wrapper for a giac list
#################################
cdef  vecteur _getgiacslice(Pygen L,slice sl) except +:
   cdef Pygen pyg=Pygen()
   cdef vecteur  * V
   cdef int u

   if (L.type()=="DOM_LIST"):
      n=len(L)
      V=new vecteur()
      ressetctrl_c()
#      sig_on()
#      for u in range(n)[sl]:   #pb python3
      (b,e,st)=sl.indices(n)
      for u in range(b,e,st):
        if(GIACctrl_c):
          raise KeyboardInterrupt,"Interrupted by a ctrl-c event"
        V.push_back((L.gptr[0])[u])
#      sig_off()
      return V[0]
   else:
     raise TypeError,"argument must be a Pygen list and a slice"





cdef  gen pylongtogen(a) except +:
   #                                                                     #
   # basic conversion of Python long integers to gen via Horner's Method #
   #                                                                     #
   ressetctrl_c()
   aneg=False
   cdef gen g=gen(<int>0)
   cdef gen M

   if (a<0):
     aneg=True
     a=-a
   if Pyversioninfo >= (2,7):
      size=a.bit_length()  # bit_length python >= 2.7 required.
      shift=Pymaxint.bit_length()-1
   else:
      size=math.trunc(math.log(a,2))+1
      shift=math.trunc(math.log(Pymaxint))
   M=gen(<long long>(1<<shift))

   while (size>=shift):
     if(GIACctrl_c):
          raise KeyboardInterrupt,"Interrupted by a ctrl-c event"
     size=size-shift
     i=int(a>>size)
     g=(g*M+gen(<long long>i))
     a=a-(i<<size)

   g=g*gen(<long long>(1<<size))+gen(<long long> a)
   if aneg:
     # g=-g doesnt cythonize with cython 0.24, (- operator not declared?)
     g=GIAC_neg(g)
   return g;



#############################################################
# Examples of python functions directly implemented from giac
#############################################################
#def giaceval(Pygen self):
#    cdef gen result
#    ressetctrl_c()
#    try:
#      result=GIAC_protecteval(self.gptr[0],1,context_ptr)
#      return _wrap_gen(result)
#    except:
#      raise
#
#
#def giacfactor(Pygen self):
#
#    cdef gen result
#    ressetctrl_c() #It's better to do this before calling giac.
#    try:
#      result=GIAC_factor(self.gptr[0],context_ptr)
#      return _wrap_gen(result)
#    except:
#      raise
#
#
#
#def giacfactors(Pygen self):
#    cdef gen result
#    ressetctrl_c()
#    try:
#      result=GIAC_factors(self.gptr[0],context_ptr)
#      return _wrap_gen(result)
#    except:
#      raise
#
#
#
#
#def giacnormal(Pygen self):
#    cdef gen result
#    ressetctrl_c()
#    try:
#      result=GIAC_normal(self.gptr[0],context_ptr)
#      return _wrap_gen(result)
#    except:
#      raise
#
#
#def giacgcd(Pygen a, Pygen b):
#    cdef gen result
#    ressetctrl_c()
#    try:
#      result=gen( GIAC_makenewvecteur(a.gptr[0],b.gptr[0]) ,<short int>1)
#      result=GIAC_gcd(result,context_ptr)
#      return _wrap_gen(result)
#    except:
#      raise



#############################################
# giac functions/keywords
#############################################

I=Pygen('i')  # The complex number sqrt(-1)


def htmlhelp(s='en'):
   """
   Open the giac html detailled help in an external  browser

   There are currently 3 supported lanquages: 'en', 'fr', 'el'
    >>> htmlhelp('fr')         # doctest: +SKIP
    >>> htmlhelp()             # doctest: +SKIP

   """
   giacbasedir=decstring23(GIAC_giac_aide_dir())  # python3
   if (not s in ['en', 'fr', 'el']):
     s='en'
   s='doc/'+s+'/cascmd_'+s+'/index.html'
   ressetctrl_c()
   try:
     #if 1==htmlbrowserhelp(s) :
     #  raise RuntimeError,'unable to launch browser'
     url=giacbasedir+s
     if not os.access(url,os.F_OK):
         url='http://www-fourier.ujf-grenoble.fr/~parisse/giac/'+s
     else:
         url='file:'+url
     wwwbrowseropen(url)
   except:
     raise


#############################################################
#  Qcas string interactive 2D geometry; string input
#############################################################
def qcas(str s):
   """
   * EXPERIMENTAL: Send a giac command to an  interactive 2D geometry display in qcas.
     Current state: Geometric objects will be displayed, but only geometric objects STORED in a giac variable can be used for interactive geometric constructions in qcas.

    >>> d1='A:=point(1+i);t:=element(10..100,1,10);C:=circle(A,t*0.05);M:=element(C);'
    >>> qcas(d1)    # doctest: +SKIP

   """
   if s=='':
      return
   else:
      oldies=Pygen('"using sendtext"')
      ressetctrl_c()
      try:
         from giacpy2qcas import toqcas
         toqcas(oldies,s)
         return
      except:
         raise RuntimeError







#############################################################
#  Most giac keywords
#############################################################
include 'keywords.pxi'
GiacMethods={}



__all__=['giac','Pygen','giacsettings','I','htmlhelp','qcas','loadgiacgen']+mostkeywords+nonevaluable


#################################################################
#  A Wrapper class to setup the __doc__ attribute from giac's doc
#################################################################

class ThreadedPygen(Pygen):
   """
   Use this subclass of to call your objects with the threadeval method.
   It is usefull to interupt a computation with control C with many python front ends.
   This class is used by GiacFunction
   """
   def __call__(self, *args):
      return self.threadeval(*args)


class GiacFunction:
   # docstring removed to show  self.__doc__  under IEP.

   def __init__(self,str s):
      if (s=='assume' or s=='supposons'):
         self.Pygen=Pygen(s)
      else:
         self.Pygen=ThreadedPygen(s)

      try:
         self.__doc__="(from giac's help:)"+Pygen('?'+s).eval().__str__()
      except:
         self.__doc__="failed to init doc from giac's doc"


   def __call__(self,*args):
      return self.Pygen(*args)


   def __repr__(self):
      return self.Pygen.__repr__()


   def __str__(self):
      return self.Pygen.__str__()


   def __add__(self,right):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self+right


   def __sub__(self,right):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self-right


   def __mul__(self,right):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self*right


   def __div__(self,right):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self/right


   def __truediv__(self,right):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self*right


   def __pow__(self,right,ignored):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self**right


   def __neg__(self):
      return -self.Pygen


   def diff(self,*args):
      return self.Pygen.diff(args)


   def int(self,*args):
      return self.Pygen.int(args)


   def plot(self,*args):
      return self.Pygen.plot(args)


   def htmlhelp(self,str lang='en'):
      return self.Pygen.htmlhelp(lang)




#############################################################
# Some convenient settings
#############################################################
Pygen('printpow(-1)').eval() ; # default power is ** instead of ^
Pygen('add_language(1)').eval() ; # Add the french keywords in the giac library language.
# FIXME: print I for sqrt(-1) instead of i
#GIAC_try_parse_i(False,context_ptr);


for i in mostkeywords:
   #print i
   #tmp=Pygen(i)
   tmp=GiacFunction(i)
   globals()[i]=tmp
   #GiacMethods[i]=tmp
   GiacMethods[i]=tmp.Pygen

# We put the giac names that should not be exported to Python in moremethods.
for i in moremethods:
   #tmp=Pygen(i)
   tmp=GiacFunction(i)
   #GiacMethods[i]=tmp
   GiacMethods[i]=tmp.Pygen

for i in nonevaluable:
#   print i
   tmp=Pygen(i)
   globals()[i]=tmp
   GiacMethods[i]=tmp
##
def moretests():
   """
     >>> from giacpy import giac
     >>> giac(3**100)
     515377520732011331036461129765621272702107522001
     >>> giac(-3**100)
     -515377520732011331036461129765621272702107522001
     >>> giac(-11**1000)
     -2469932918005826334124088385085221477709733385238396234869182951830739390375433175367866116456946191973803561189036523363533798726571008961243792655536655282201820357872673322901148243453211756020067624545609411212063417307681204817377763465511222635167942816318177424600927358163388910854695041070577642045540560963004207926938348086979035423732739933235077042750354729095729602516751896320598857608367865475244863114521391548985943858154775884418927768284663678512441565517194156946312753546771163991252528017732162399536497445066348868438762510366191040118080751580689254476068034620047646422315123643119627205531371694188794408120267120500325775293645416335230014278578281272863450085145349124727476223298887655183167465713337723258182649072572861625150703747030550736347589416285606367521524529665763903537989935510874657420361426804068643262800901916285076966174176854351055183740078763891951775452021781225066361670593917001215032839838911476044840388663443684517735022039957481918726697789827894303408292584258328090724141496484460001
    >>> v=[1,58,1387,17715,131260,578697,1538013,2648041,3687447,4993299,5858116,5979221,5239798,4098561,3176188,1660466,705432]
    >>> giac(v)*v
    175925584603774
    >>> giac([v])*(giac([v]).transpose())
    matrix[[175925584603774]]
    >>> v=giac('pari()')
    >>> if len(v)>200:
    ...    giac('pari(18446744073709551616)')
    ... else:
    ...    giac('2^64')
    18446744073709551616

    Testing substraction of table/sparse matrix
    >>> A=giacpy.table(())
    >>> B=giacpy.table([[1]])
    >>> A-B
    table(
    (0,0) = -1
    )
 
   """
   return



def loadgiacgen(str filename):
        """
          Open a file in giac compressed format to create a Pygen element.

          Use the save method from Pygen elements to create such files.

          In C++ these files can be opened with giac::unarchive and created with
          giac::archive

            >>> from giacpy import *
            >>> g=texpand('tan(10*a+3*b)')
            >>> g.save("fichiertest")           #  doctest: +SKIP
            >>> a=loadgiacgen("fichiertest")    #  doctest: +SKIP

        """
        cdef gen result
        ressetctrl_c()
        try:
            result=GIAC_unarchive( <string>encstring23(filename), context_ptr)
            return _wrap_gen(result)
        except:
             raise RuntimeError
