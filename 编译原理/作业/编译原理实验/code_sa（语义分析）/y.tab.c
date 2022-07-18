/* A Bison parser, made by GNU Bison 3.5.1.  */

/* Bison implementation for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2020 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Undocumented macros, especially those whose name start with YY_,
   are private implementation details.  Do not rely on them.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "3.5.1"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1




/* First part of user prologue.  */
#line 1 "ga.y"

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include "df.h"

#define YYSTYPE Node*

FILE* yyin;
int yylex(void);
void yyerror(const char *s);

// 根节点
Node* root = NULL;

// 符号表
Symbol symbolTable[TABLE_SIZE];
int symbolNum = 0;

char* type_string[6] = {"null", "int", "float", "char", "string", "bool"};

// 可视化语法树的代码串
char map[100000] = "digraph demo{\nnode [shape=box, style=\"rounded\", color=\"black\", fontname=\"Microsoft YaHei\"];\nedge [fontname=\"Microsoft YaHei\"];\n";
int id = 0;


// 中间代码生成：临时标号申请
int label_id = 0;
int newLabel();
// 中间代码生成：临时变量申请
int temp_id = 0;
int newTempID();
// 因为我们有节点的全局ID 中间代码中每一个为定义next标号可以先用全局ID给他标记下来
// 这样对于一个中间代码文本中，我们可以找到他，并识别他的原本在语法树中的节点。
// 我们遍历一遍树，将必要的next = $$->next自顶向下更新，同时我们每更新一个节点，就去中间代码串中寻找他的位置，并修改成我们新赋值的next值。
void UpdateNext(Node* root, char code[]);


#line 110 "y.tab.c"

# ifndef YY_CAST
#  ifdef __cplusplus
#   define YY_CAST(Type, Val) static_cast<Type> (Val)
#   define YY_REINTERPRET_CAST(Type, Val) reinterpret_cast<Type> (Val)
#  else
#   define YY_CAST(Type, Val) ((Type) (Val))
#   define YY_REINTERPRET_CAST(Type, Val) ((Type) (Val))
#  endif
# endif
# ifndef YY_NULLPTR
#  if defined __cplusplus
#   if 201103L <= __cplusplus
#    define YY_NULLPTR nullptr
#   else
#    define YY_NULLPTR 0
#   endif
#  else
#   define YY_NULLPTR ((void*)0)
#  endif
# endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 1
#endif

/* Use api.header.include to #include this header
   instead of duplicating it here.  */
#ifndef YY_YY_Y_TAB_H_INCLUDED
# define YY_YY_Y_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    INT = 258,
    FLOAT = 259,
    CHAR = 260,
    STRING = 261,
    BOOL = 262,
    ID = 263,
    WHILE = 264,
    DO = 265,
    IF = 266,
    THEN = 267,
    ELSE = 268,
    END = 269,
    REPEAT = 270,
    UNTIL = 271,
    READ = 272,
    WRITE = 273,
    TRUE = 274,
    FALSE = 275,
    TYPE = 276,
    LE = 277,
    GE = 278,
    ASSIGN = 279,
    OR = 280,
    AND = 281,
    NOT = 282
  };
#endif
/* Tokens.  */
#define INT 258
#define FLOAT 259
#define CHAR 260
#define STRING 261
#define BOOL 262
#define ID 263
#define WHILE 264
#define DO 265
#define IF 266
#define THEN 267
#define ELSE 268
#define END 269
#define REPEAT 270
#define UNTIL 271
#define READ 272
#define WRITE 273
#define TRUE 274
#define FALSE 275
#define TYPE 276
#define LE 277
#define GE 278
#define ASSIGN 279
#define OR 280
#define AND 281
#define NOT 282

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_Y_TAB_H_INCLUDED  */



#ifdef short
# undef short
#endif

/* On compilers that do not define __PTRDIFF_MAX__ etc., make sure
   <limits.h> and (if available) <stdint.h> are included
   so that the code can choose integer types of a good width.  */

#ifndef __PTRDIFF_MAX__
# include <limits.h> /* INFRINGES ON USER NAME SPACE */
# if defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stdint.h> /* INFRINGES ON USER NAME SPACE */
#  define YY_STDINT_H
# endif
#endif

/* Narrow types that promote to a signed type and that can represent a
   signed or unsigned integer of at least N bits.  In tables they can
   save space and decrease cache pressure.  Promoting to a signed type
   helps avoid bugs in integer arithmetic.  */

#ifdef __INT_LEAST8_MAX__
typedef __INT_LEAST8_TYPE__ yytype_int8;
#elif defined YY_STDINT_H
typedef int_least8_t yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef __INT_LEAST16_MAX__
typedef __INT_LEAST16_TYPE__ yytype_int16;
#elif defined YY_STDINT_H
typedef int_least16_t yytype_int16;
#else
typedef short yytype_int16;
#endif

#if defined __UINT_LEAST8_MAX__ && __UINT_LEAST8_MAX__ <= __INT_MAX__
typedef __UINT_LEAST8_TYPE__ yytype_uint8;
#elif (!defined __UINT_LEAST8_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST8_MAX <= INT_MAX)
typedef uint_least8_t yytype_uint8;
#elif !defined __UINT_LEAST8_MAX__ && UCHAR_MAX <= INT_MAX
typedef unsigned char yytype_uint8;
#else
typedef short yytype_uint8;
#endif

#if defined __UINT_LEAST16_MAX__ && __UINT_LEAST16_MAX__ <= __INT_MAX__
typedef __UINT_LEAST16_TYPE__ yytype_uint16;
#elif (!defined __UINT_LEAST16_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST16_MAX <= INT_MAX)
typedef uint_least16_t yytype_uint16;
#elif !defined __UINT_LEAST16_MAX__ && USHRT_MAX <= INT_MAX
typedef unsigned short yytype_uint16;
#else
typedef int yytype_uint16;
#endif

#ifndef YYPTRDIFF_T
# if defined __PTRDIFF_TYPE__ && defined __PTRDIFF_MAX__
#  define YYPTRDIFF_T __PTRDIFF_TYPE__
#  define YYPTRDIFF_MAXIMUM __PTRDIFF_MAX__
# elif defined PTRDIFF_MAX
#  ifndef ptrdiff_t
#   include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  endif
#  define YYPTRDIFF_T ptrdiff_t
#  define YYPTRDIFF_MAXIMUM PTRDIFF_MAX
# else
#  define YYPTRDIFF_T long
#  define YYPTRDIFF_MAXIMUM LONG_MAX
# endif
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned
# endif
#endif

#define YYSIZE_MAXIMUM                                  \
  YY_CAST (YYPTRDIFF_T,                                 \
           (YYPTRDIFF_MAXIMUM < YY_CAST (YYSIZE_T, -1)  \
            ? YYPTRDIFF_MAXIMUM                         \
            : YY_CAST (YYSIZE_T, -1)))

#define YYSIZEOF(X) YY_CAST (YYPTRDIFF_T, sizeof (X))

/* Stored state numbers (used for stacks). */
typedef yytype_int8 yy_state_t;

/* State numbers in computations.  */
typedef int yy_state_fast_t;

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif

#ifndef YY_ATTRIBUTE_PURE
# if defined __GNUC__ && 2 < __GNUC__ + (96 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_PURE __attribute__ ((__pure__))
# else
#  define YY_ATTRIBUTE_PURE
# endif
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# if defined __GNUC__ && 2 < __GNUC__ + (7 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_UNUSED __attribute__ ((__unused__))
# else
#  define YY_ATTRIBUTE_UNUSED
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(E) ((void) (E))
#else
# define YYUSE(E) /* empty */
#endif

#if defined __GNUC__ && ! defined __ICC && 407 <= __GNUC__ * 100 + __GNUC_MINOR__
/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                            \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")              \
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# define YY_IGNORE_MAYBE_UNINITIALIZED_END      \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif

#if defined __cplusplus && defined __GNUC__ && ! defined __ICC && 6 <= __GNUC__
# define YY_IGNORE_USELESS_CAST_BEGIN                          \
    _Pragma ("GCC diagnostic push")                            \
    _Pragma ("GCC diagnostic ignored \"-Wuseless-cast\"")
# define YY_IGNORE_USELESS_CAST_END            \
    _Pragma ("GCC diagnostic pop")
#endif
#ifndef YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_END
#endif


#define YY_ASSERT(E) ((void) (0 && (E)))

#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yy_state_t yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (YYSIZEOF (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (YYSIZEOF (yy_state_t) + YYSIZEOF (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYPTRDIFF_T yynewbytes;                                         \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * YYSIZEOF (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / YYSIZEOF (*yyptr);                        \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, YY_CAST (YYSIZE_T, (Count)) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYPTRDIFF_T yyi;                      \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  34
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   117

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  41
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  12
/* YYNRULES -- Number of rules.  */
#define YYNRULES  41
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  83

#define YYUNDEFTOK  2
#define YYMAXUTOK   282


/* YYTRANSLATE(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, with out-of-bounds checking.  */
#define YYTRANSLATE(YYX)                                                \
  (0 <= (YYX) && (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex.  */
static const yytype_int8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      27,    28,    35,    33,    25,    34,     2,    36,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,    26,
      31,    40,    32,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,    29,     2,    30,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      37,    38,    39
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_int16 yyrline[] =
{
       0,    60,    60,    71,    82,    86,    93,   103,   107,   113,
     121,   138,   172,   192,   222,   251,   269,   278,   294,   297,
     300,   304,   314,   324,   334,   353,   388,   423,   458,   494,
     504,   517,   530,   544,   558,   573,   583,   595,   626,   658,
     690,   722
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 1
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "INT", "FLOAT", "CHAR", "STRING", "BOOL",
  "ID", "WHILE", "DO", "IF", "THEN", "ELSE", "END", "REPEAT", "UNTIL",
  "READ", "WRITE", "TRUE", "FALSE", "TYPE", "LE", "GE", "ASSIGN", "','",
  "';'", "'('", "')'", "'{'", "'}'", "'<'", "'>'", "'+'", "'-'", "'*'",
  "'/'", "OR", "AND", "NOT", "'='", "$accept", "program", "declarations",
  "declaration", "varlist", "stmt", "xstmt", "exp", "arithmeticexp",
  "boolexp", "strexp", "comparison", YY_NULLPTR
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[NUM] -- (External) token number corresponding to the
   (internal) symbol number NUM (which must be that of a token).  */
static const yytype_int16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,    44,    59,    40,    41,   123,
     125,    60,    62,    43,    45,    42,    47,   280,   281,   282,
      61
};
# endif

#define YYPACT_NINF (-25)

#define yypact_value_is_default(Yyn) \
  ((Yyn) == YYPACT_NINF)

#define YYTABLE_NINF (-1)

#define yytable_value_is_error(Yyn) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int8 yypact[] =
{
      94,   -17,    27,    27,    99,     6,    19,     9,    20,    99,
      25,   -25,    31,    19,   -25,   -25,   -25,   -25,    27,    27,
      64,    11,   -25,    24,    16,   -25,   -25,   -25,   -25,    64,
      -9,   -25,    38,   -25,   -25,   -25,    44,    99,   -25,    45,
     -22,   -25,    56,    56,    56,    56,    56,    56,    56,    56,
      56,    99,    27,    27,    99,    27,     9,   -25,   -25,   -25,
     -25,    56,    36,    36,    36,    36,    53,    53,   -25,   -25,
      36,    60,    46,   -25,    77,    -9,   -25,   -24,   -25,    99,
     -25,    68,   -25
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_int8 yydefact[] =
{
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     3,     0,     0,    21,    22,    29,    23,     0,     0,
       0,     0,    30,     0,     0,    16,    35,    36,    17,    18,
      19,    20,     7,     6,     1,     2,     4,     9,    15,     0,
       0,    32,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     5,    10,    24,
      31,     0,    41,    40,    38,    37,    25,    26,    27,    28,
      39,     0,    34,    33,     0,    14,     8,     0,    13,     0,
      12,     0,    11
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int8 yypgoto[] =
{
     -25,   -25,    57,   -25,    50,    -4,   -25,    79,    -5,     0,
     -25,   -25
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int8 yydefgoto[] =
{
      -1,     8,     9,    10,    33,    11,    12,    28,    20,    30,
      31,    22
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int8 yytable[] =
{
      24,    29,    21,    23,    59,    35,    60,    13,    29,    46,
      47,    48,    49,    39,    25,    52,    53,    32,    40,    41,
      34,    51,    14,    15,    26,    27,    16,    17,    52,    53,
      14,    15,    55,    58,    16,    17,    54,    62,    63,    64,
      65,    66,    67,    68,    69,    70,    18,    71,    52,    53,
      74,    36,    72,    73,    18,    75,    77,    37,    19,    14,
      15,    52,    53,    56,    17,     7,    19,    42,    43,    46,
      47,    48,    49,    59,    78,    81,    44,    45,    46,    47,
      48,    49,    82,    61,    53,    50,    42,    43,    48,    49,
      79,    80,    38,    57,     0,    44,    45,    46,    47,    48,
      49,     0,     1,     2,    50,     3,    76,     1,     2,     4,
       3,     5,     6,     0,     4,     7,     5,     6
};

static const yytype_int8 yycheck[] =
{
       4,     6,     2,     3,    28,     9,    28,    24,    13,    33,
      34,    35,    36,    18,     8,    37,    38,     8,    18,    19,
       0,    10,     3,     4,     5,     6,     7,     8,    37,    38,
       3,     4,    16,    37,     7,     8,    12,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    27,    51,    37,    38,
      54,    26,    52,    53,    27,    55,    61,    26,    39,     3,
       4,    37,    38,    25,     8,    21,    39,    22,    23,    33,
      34,    35,    36,    28,    14,    79,    31,    32,    33,    34,
      35,    36,    14,    27,    38,    40,    22,    23,    35,    36,
      13,    14,    13,    36,    -1,    31,    32,    33,    34,    35,
      36,    -1,     8,     9,    40,    11,    56,     8,     9,    15,
      11,    17,    18,    -1,    15,    21,    17,    18
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_int8 yystos[] =
{
       0,     8,     9,    11,    15,    17,    18,    21,    42,    43,
      44,    46,    47,    24,     3,     4,     7,     8,    27,    39,
      49,    50,    52,    50,    46,     8,     5,     6,    48,    49,
      50,    51,     8,    45,     0,    46,    26,    26,    48,    49,
      50,    50,    22,    23,    31,    32,    33,    34,    35,    36,
      40,    10,    37,    38,    12,    16,    25,    43,    46,    28,
      28,    27,    49,    49,    49,    49,    49,    49,    49,    49,
      49,    46,    50,    50,    46,    50,    45,    49,    14,    13,
      14,    46,    14
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_int8 yyr1[] =
{
       0,    41,    42,    42,    43,    43,    44,    45,    45,    46,
      46,    47,    47,    47,    47,    47,    47,    47,    48,    48,
      48,    49,    49,    49,    49,    49,    49,    49,    49,    50,
      50,    50,    50,    50,    50,    51,    51,    52,    52,    52,
      52,    52
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_int8 yyr2[] =
{
       0,     2,     2,     1,     2,     3,     2,     1,     3,     2,
       3,     7,     5,     5,     4,     3,     2,     2,     1,     1,
       1,     1,     1,     1,     3,     3,     3,     3,     3,     1,
       1,     3,     2,     3,     3,     1,     1,     3,     3,     3,
       3,     3
};


#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)
#define YYEMPTY         (-2)
#define YYEOF           0

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                    \
  do                                                              \
    if (yychar == YYEMPTY)                                        \
      {                                                           \
        yychar = (Token);                                         \
        yylval = (Value);                                         \
        YYPOPSTACK (yylen);                                       \
        yystate = *yyssp;                                         \
        goto yybackup;                                            \
      }                                                           \
    else                                                          \
      {                                                           \
        yyerror (YY_("syntax error: cannot back up")); \
        YYERROR;                                                  \
      }                                                           \
  while (0)

/* Error token number */
#define YYTERROR        1
#define YYERRCODE       256



/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)

/* This macro is provided for backward compatibility. */
#ifndef YY_LOCATION_PRINT
# define YY_LOCATION_PRINT(File, Loc) ((void) 0)
#endif


# define YY_SYMBOL_PRINT(Title, Type, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Type, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*-----------------------------------.
| Print this symbol's value on YYO.  |
`-----------------------------------*/

static void
yy_symbol_value_print (FILE *yyo, int yytype, YYSTYPE const * const yyvaluep)
{
  FILE *yyoutput = yyo;
  YYUSE (yyoutput);
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyo, yytoknum[yytype], *yyvaluep);
# endif
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/*---------------------------.
| Print this symbol on YYO.  |
`---------------------------*/

static void
yy_symbol_print (FILE *yyo, int yytype, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyo, "%s %s (",
             yytype < YYNTOKENS ? "token" : "nterm", yytname[yytype]);

  yy_symbol_value_print (yyo, yytype, yyvaluep);
  YYFPRINTF (yyo, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yy_state_t *yybottom, yy_state_t *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yy_state_t *yyssp, YYSTYPE *yyvsp, int yyrule)
{
  int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %d):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       yystos[+yyssp[yyi + 1 - yynrhs]],
                       &yyvsp[(yyi + 1) - (yynrhs)]
                                              );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen(S) (YY_CAST (YYPTRDIFF_T, strlen (S)))
#  else
/* Return the length of YYSTR.  */
static YYPTRDIFF_T
yystrlen (const char *yystr)
{
  YYPTRDIFF_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
static char *
yystpcpy (char *yydest, const char *yysrc)
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYPTRDIFF_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYPTRDIFF_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
        switch (*++yyp)
          {
          case '\'':
          case ',':
            goto do_not_strip_quotes;

          case '\\':
            if (*++yyp != '\\')
              goto do_not_strip_quotes;
            else
              goto append;

          append:
          default:
            if (yyres)
              yyres[yyn] = *yyp;
            yyn++;
            break;

          case '"':
            if (yyres)
              yyres[yyn] = '\0';
            return yyn;
          }
    do_not_strip_quotes: ;
    }

  if (yyres)
    return yystpcpy (yyres, yystr) - yyres;
  else
    return yystrlen (yystr);
}
# endif

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return 1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return 2 if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYPTRDIFF_T *yymsg_alloc, char **yymsg,
                yy_state_t *yyssp, int yytoken)
{
  enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
  /* Internationalized format string. */
  const char *yyformat = YY_NULLPTR;
  /* Arguments of yyformat: reported tokens (one for the "unexpected",
     one per "expected"). */
  char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
  /* Actual size of YYARG. */
  int yycount = 0;
  /* Cumulated lengths of YYARG.  */
  YYPTRDIFF_T yysize = 0;

  /* There are many possibilities here to consider:
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yytoken != YYEMPTY)
    {
      int yyn = yypact[+*yyssp];
      YYPTRDIFF_T yysize0 = yytnamerr (YY_NULLPTR, yytname[yytoken]);
      yysize = yysize0;
      yyarg[yycount++] = yytname[yytoken];
      if (!yypact_value_is_default (yyn))
        {
          /* Start YYX at -YYN if negative to avoid negative indexes in
             YYCHECK.  In other words, skip the first -YYN actions for
             this state because they are default actions.  */
          int yyxbegin = yyn < 0 ? -yyn : 0;
          /* Stay within bounds of both yycheck and yytname.  */
          int yychecklim = YYLAST - yyn + 1;
          int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
          int yyx;

          for (yyx = yyxbegin; yyx < yyxend; ++yyx)
            if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR
                && !yytable_value_is_error (yytable[yyx + yyn]))
              {
                if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                  {
                    yycount = 1;
                    yysize = yysize0;
                    break;
                  }
                yyarg[yycount++] = yytname[yyx];
                {
                  YYPTRDIFF_T yysize1
                    = yysize + yytnamerr (YY_NULLPTR, yytname[yyx]);
                  if (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM)
                    yysize = yysize1;
                  else
                    return 2;
                }
              }
        }
    }

  switch (yycount)
    {
# define YYCASE_(N, S)                      \
      case N:                               \
        yyformat = S;                       \
      break
    default: /* Avoid compiler warnings. */
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
# undef YYCASE_
    }

  {
    /* Don't count the "%s"s in the final size, but reserve room for
       the terminator.  */
    YYPTRDIFF_T yysize1 = yysize + (yystrlen (yyformat) - 2 * yycount) + 1;
    if (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM)
      yysize = yysize1;
    else
      return 2;
  }

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return 1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yyarg[yyi++]);
          yyformat += 2;
        }
      else
        {
          ++yyp;
          ++yyformat;
        }
  }
  return 0;
}
#endif /* YYERROR_VERBOSE */

/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
{
  YYUSE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}




/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;


/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    yy_state_fast_t yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       'yyss': related to states.
       'yyvs': related to semantic values.

       Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yy_state_t yyssa[YYINITDEPTH];
    yy_state_t *yyss;
    yy_state_t *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    YYPTRDIFF_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken = 0;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYPTRDIFF_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yyssp = yyss = yyssa;
  yyvsp = yyvs = yyvsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */
  goto yysetstate;


/*------------------------------------------------------------.
| yynewstate -- push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;


/*--------------------------------------------------------------------.
| yysetstate -- set current state (the top of the stack) to yystate.  |
`--------------------------------------------------------------------*/
yysetstate:
  YYDPRINTF ((stderr, "Entering state %d\n", yystate));
  YY_ASSERT (0 <= yystate && yystate < YYNSTATES);
  YY_IGNORE_USELESS_CAST_BEGIN
  *yyssp = YY_CAST (yy_state_t, yystate);
  YY_IGNORE_USELESS_CAST_END

  if (yyss + yystacksize - 1 <= yyssp)
#if !defined yyoverflow && !defined YYSTACK_RELOCATE
    goto yyexhaustedlab;
#else
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYPTRDIFF_T yysize = yyssp - yyss + 1;

# if defined yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        yy_state_t *yyss1 = yyss;
        YYSTYPE *yyvs1 = yyvs;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * YYSIZEOF (*yyssp),
                    &yyvs1, yysize * YYSIZEOF (*yyvsp),
                    &yystacksize);
        yyss = yyss1;
        yyvs = yyvs1;
      }
# else /* defined YYSTACK_RELOCATE */
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yy_state_t *yyss1 = yyss;
        union yyalloc *yyptr =
          YY_CAST (union yyalloc *,
                   YYSTACK_ALLOC (YY_CAST (YYSIZE_T, YYSTACK_BYTES (yystacksize))));
        if (! yyptr)
          goto yyexhaustedlab;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
# undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YY_IGNORE_USELESS_CAST_BEGIN
      YYDPRINTF ((stderr, "Stack size increased to %ld\n",
                  YY_CAST (long, yystacksize)));
      YY_IGNORE_USELESS_CAST_END

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }
#endif /* !defined yyoverflow && !defined YYSTACK_RELOCATE */

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;


/*-----------.
| yybackup.  |
`-----------*/
yybackup:
  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);
  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  /* Discard the shifted token.  */
  yychar = YYEMPTY;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
  case 2:
#line 61 "ga.y"
        { 
		yyval = genNode("program", 0); 
		addChild(yyval, yyvsp[-1]);
		addChild(yyval, yyvsp[0]);
		root = yyval;

		// 中间代码生成
		strcpy(yyval->code, yyvsp[0]->code);
		UpdateNext(root, root->code);
	}
#line 1454 "y.tab.c"
    break;

  case 3:
#line 72 "ga.y"
        { 
		yyval = genNode("program", 0); 
		addChild(yyval, yyvsp[0]);
		root = yyval; 

		// 中间代码生成
		strcpy(yyval->code, yyvsp[0]->code);
		UpdateNext(root, root->code);
	}
#line 1468 "y.tab.c"
    break;

  case 4:
#line 82 "ga.y"
                              {
		yyval = genNode("declarations", 0); 
		addChild(yyval, yyvsp[-1]);
	}
#line 1477 "y.tab.c"
    break;

  case 5:
#line 87 "ga.y"
        { 
		yyval = genNode("declarations", 0); 
		addChild(yyval, yyvsp[-2]);
		addChild(yyval, yyvsp[0]);
	}
#line 1487 "y.tab.c"
    break;

  case 6:
#line 94 "ga.y"
    { 
		yyval = genNode("declaration", 0); 
		addChild(yyval, yyvsp[-1]);
		addChild(yyval, yyvsp[0]);
		
		// 生成符号表
		updateSymbolTable(yyval); 
	}
#line 1500 "y.tab.c"
    break;

  case 7:
#line 103 "ga.y"
            { 
		yyval = genNode("varlist", 0);  
		addChild(yyval, yyvsp[0]);
	}
#line 1509 "y.tab.c"
    break;

  case 8:
#line 107 "ga.y"
                     {
		yyval = genNode("varlist", 0); 
		addChild(yyval, yyvsp[-2]);
		addChild(yyval, yyvsp[0]);
	}
#line 1519 "y.tab.c"
    break;

  case 9:
#line 113 "ga.y"
                {
		yyval = genNode("xstmt", 0); 
		addChild(yyval, yyvsp[-1]);

		// 中间代码生成
		yyvsp[-1]->next = yyval->next;
		strcpy(yyval->code, yyvsp[-1]->code);
	}
#line 1532 "y.tab.c"
    break;

  case 10:
#line 121 "ga.y"
                     {
		yyval = genNode("xstmt", 0); 
		addChild(yyval, yyvsp[-2]);
		addChild(yyval, yyvsp[0]);

		// 中间代码生成
		yyvsp[-2]->next = newLabel(); // L 属性赋初始值的地方

		// $$->code = $1->code || Label $1->next || $3->code
		strcpy(yyval->code, yyvsp[-2]->code);
		char labelcode[25];
		sprintf(labelcode, "Label %03d:\n", yyvsp[-2]->next);
		strcat(yyval->code, labelcode);
		strcat(yyval->code, yyvsp[0]->code);
	}
#line 1552 "y.tab.c"
    break;

  case 11:
#line 138 "ga.y"
                                          {
		yyval = genNode("xstmt", 0); 
		addChild(yyval, yyvsp[-6]);  addChild(yyval, yyvsp[-5]); addChild(yyval, yyvsp[-4]);  addChild(yyval, yyvsp[-3]);
		addChild(yyval, yyvsp[-2]);  addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);

		// 中间代码生成
		int fabegin = newLabel();
		// $$->code = $2->code || "If-not _t($2->t_id) Goto Label fabegin" || $4->code 
		// 			  || Goto $$->next || Label fabegin || $6->code

		strcpy(yyval->code, yyvsp[-5]->code);
		char ifnotcode[100];

		if(yyval->next != -1){
			sprintf(ifnotcode, "If-not _t%d Goto Label %03d\n", yyvsp[-5]->t_id, yyval->next);
		}
		else{
			sprintf(ifnotcode, "If-not _t%d Goto __Label %03d__\n", yyvsp[-5]->t_id, yyval->children[0]->id);
		}
		
		strcat(yyval->code, ifnotcode);
		strcat(yyval->code, yyvsp[-3]->code);
		char labelcode[25];
		if(yyval->next != -1){
			sprintf(labelcode, "Goto Label %03d\n", yyval->next);
		}
		else{
			sprintf(labelcode, "Goto __Label %03d__\n", yyval->children[0]->id);
		}

		strcat(yyval->code, labelcode);
		sprintf(labelcode, "Label %03d:\n", fabegin);
		strcat(yyval->code, yyvsp[-1]->code);
	}
#line 1591 "y.tab.c"
    break;

  case 12:
#line 172 "ga.y"
                               {
		yyval = genNode("xstmt", 0); 
		addChild(yyval, yyvsp[-4]); addChild(yyval, yyvsp[-3]); addChild(yyval, yyvsp[-2]);
		addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);

		// 中间代码生成
		// $$->code = $2->code || "If-not _t($2->t_id) Goto Label $$->next" || $4->code
		strcpy(yyval->code, yyvsp[-3]->code);
		char ifnotcode[100];
		
		if(yyval->next != -1){
			sprintf(ifnotcode, "If-not _t%d Goto Label %03d\n", yyvsp[-3]->t_id, yyval->next);
		}
		else{
			sprintf(ifnotcode, "If-not _t%d Goto __Label %03d__\n", yyvsp[-3]->t_id, yyval->children[0]->id);
		}
		
		strcat(yyval->code, ifnotcode);
		strcat(yyval->code, yyvsp[-1]->code);
	}
#line 1616 "y.tab.c"
    break;

  case 13:
#line 192 "ga.y"
                                {
		yyval = genNode("xstmt", 0); 
		addChild(yyval, yyvsp[-4]); addChild(yyval, yyvsp[-3]); addChild(yyval, yyvsp[-2]);
		addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);

		// 中间代码生成
		int begin = newLabel();
		// $$->code = Label begin || $2->code || "If-not _t($2->t_id) Goto Label $$->next"
		//            || $4->code || Goto begin
		char labelcode[25];
		sprintf(labelcode, "Label %03d:\n", begin);
		strcpy(yyval->code, labelcode);
		strcat(yyval->code, yyvsp[-3]->code);

		char ifnotcode[100];

		if(yyval->next != -1){
			sprintf(ifnotcode, "If-not _t%d Goto Label %03d\n", yyvsp[-3]->t_id, yyval->next);
		}
		else{
			sprintf(ifnotcode, "If-not _t%d Goto __Label %03d__\n", yyvsp[-3]->t_id, yyval->children[0]->id);
		}

		strcat(yyval->code, ifnotcode);

		strcat(yyval->code, yyvsp[-1]->code);
		sprintf(labelcode, "Goto Label %03d\n", begin);
		strcat(yyval->code, labelcode);
		
	}
#line 1651 "y.tab.c"
    break;

  case 14:
#line 222 "ga.y"
                                {
		yyval = genNode("xstmt", 0); 
		addChild(yyval, yyvsp[-3]); addChild(yyval, yyvsp[-2]); addChild(yyval, yyvsp[-1]);
		addChild(yyval, yyvsp[0]);

		// 中间代码生成
		int begin = newLabel();
		// $$->code = Label begin || $2->code || $4->code || "If-not _t($4->t_id) Goto $$->next || Goto Label begin"
		char labelcode[25];
		sprintf(labelcode, "Label %03d:\n", begin);
		strcpy(yyval->code, labelcode);

		strcat(yyval->code, yyvsp[-2]->code);
		strcat(yyval->code, yyvsp[0]->code);

		char ifcode[100];
		if(yyval->next != -1){
			sprintf(ifcode, "If _t%d Goto Label %03d\n", yyvsp[0]->t_id, yyval->next);
		}
		else{
			sprintf(ifcode, "If _t%d Goto __Label %03d__\n", yyvsp[0]->t_id, yyval->children[0]->id);
		}

		strcat(yyval->code, ifcode);

		sprintf(labelcode, "Goto Label %03d\n", begin);
		strcat(yyval->code, labelcode);

	}
#line 1685 "y.tab.c"
    break;

  case 15:
#line 251 "ga.y"
                    {
		checkID(yyvsp[-2]); // 检查 ID 是否在符号表中
		checkType(yyvsp[-2], yyvsp[0], 2); // 检查类型是否匹配
		yyval = genNode("xstmt", 0); 
		addChild(yyval, yyvsp[-2]); addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);

		// 中间代码生成
		// $$->code = $3->code || "$1->name = $3->name"
		strcpy(yyval->code, yyvsp[0]->code);
		char newcode[25];
		if(yyvsp[0]->t_id == -1){ // 若 exp 为 ID
			sprintf(newcode, "%s = %s\n", yyvsp[-2]->content, yyvsp[0]->content);
		} else{
			sprintf(newcode, "%s = _t%d\n", yyvsp[-2]->content, yyvsp[0]->t_id);
		}
		strcat(yyval->code, newcode);
		
	}
#line 1708 "y.tab.c"
    break;

  case 16:
#line 269 "ga.y"
              {
		checkID(yyvsp[0]); // 检查 ID 是否在符号表中
		yyval = genNode("xstmt", 0); 
		addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);

		// 中间代码生成
		// $$->code = "Read $2->name"
		sprintf(yyval->code, "Read %s\n", yyvsp[0]->content);
	}
#line 1722 "y.tab.c"
    break;

  case 17:
#line 278 "ga.y"
                {
		yyval = genNode("writexstmt", 0); 
		addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);

		// 中间代码生成
		// $$->code = $2->code || "Write $2->name"
		strcat(yyval->code, yyvsp[0]->code);
		char newcode[25];
		if(yyvsp[0]->t_id == -1){ // 若 exp 为 ID
			sprintf(newcode, "Write %s\n", yyvsp[0]->content);
		} else{
			sprintf(newcode, "Write _t%d\n", yyvsp[0]->t_id);
		}
		strcat(yyval->code, newcode);
	}
#line 1742 "y.tab.c"
    break;

  case 18:
#line 294 "ga.y"
                   {
		yyval = yyvsp[0];
	}
#line 1750 "y.tab.c"
    break;

  case 19:
#line 297 "ga.y"
              {
		yyval = yyvsp[0];
	}
#line 1758 "y.tab.c"
    break;

  case 20:
#line 300 "ga.y"
             {
		yyval = yyvsp[0];
	}
#line 1766 "y.tab.c"
    break;

  case 21:
#line 304 "ga.y"
                   {
		yyval = genNode(yyvsp[0]->content, 0); 
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_int);

		// 中间代码生成
		// $$->code = "t1 = 123"
		yyval->t_id = newTempID();
		sprintf(yyval->code, "_t%d = %s\n", yyval->t_id, yyval->content);
	}
#line 1781 "y.tab.c"
    break;

  case 22:
#line 314 "ga.y"
            {
		yyval = genNode(yyvsp[0]->content, 0); 
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_float);

		// 中间代码生成
		// $$->code = "t1 = 1.23"
		yyval->t_id = newTempID();
		sprintf(yyval->code, "_t%d = %s\n", yyval->t_id, yyval->content);
	}
#line 1796 "y.tab.c"
    break;

  case 23:
#line 324 "ga.y"
             {
		checkID(yyvsp[0]); // 检查 ID 是否在符号表中
		yyval = genNode(yyvsp[0]->content, 0); 
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, yyvsp[0]->type);

		// 中间代码生成
		// Do nothing
		
	}
#line 1811 "y.tab.c"
    break;

  case 24:
#line 334 "ga.y"
                            {
		yyval = genNode("arithexp", 0); 
		addChild(yyval, yyvsp[-2]);
		addChild(yyval, yyvsp[-1]);
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, yyvsp[-1]->type);

		// 中间代码生成
		// $$->code = $2->code || "$$->name = $2->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[-1]->code);
		char newcode[25];
		if(yyvsp[-1]->t_id == -1){ // 若 $2 为 ID
			sprintf(newcode, "_t%d = %s\n", yyval->t_id , yyvsp[-1]->content);
		} else{
			sprintf(newcode, "_t%d = _t%d\n", yyval->t_id , yyvsp[-1]->t_id);
		}
		strcat(yyval->code, newcode);
	}
#line 1835 "y.tab.c"
    break;

  case 25:
#line 353 "ga.y"
                                      {
		checkType(yyvsp[-2], yyvsp[0], 1); // 检查类型是否匹配
		yyval = genNode("arithexp", 0); 
		addChild(yyval, yyvsp[-2]);
		addChild(yyval, yyvsp[-1]);
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, yyvsp[-2]->type);

		// 中间代码生成
		// $$->code = $3->code || $1->code || "$1->name + $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[0]->code);
		strcat(yyval->code, yyvsp[-2]->code);

		char newcode[25];
		sprintf(newcode, "_t%d = ", yyval->t_id);
		if(yyvsp[-2]->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, yyvsp[-2]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[-2]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " + ");
		if(yyvsp[0]->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, yyvsp[0]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[0]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");

		strcat(yyval->code, newcode);
	}
#line 1875 "y.tab.c"
    break;

  case 26:
#line 388 "ga.y"
                                      {
		checkType(yyvsp[-2], yyvsp[0], 1); // 检查类型是否匹配
		yyval = genNode("arithexp", 0); 
		addChild(yyval, yyvsp[-2]);
		addChild(yyval, yyvsp[-1]);
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, yyvsp[-2]->type);

		// 中间代码生成
		// $$->code = $3->code || $1->code || "$1->name - $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[0]->code);
		strcat(yyval->code, yyvsp[-2]->code);

		char newcode[25];
		sprintf(newcode, "_t%d = ", yyval->t_id);
		if(yyvsp[-2]->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, yyvsp[-2]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[-2]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " - ");
		if(yyvsp[0]->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, yyvsp[0]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[0]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat(yyval->code, newcode);
	}
#line 1915 "y.tab.c"
    break;

  case 27:
#line 423 "ga.y"
                                      {
		checkType(yyvsp[-2], yyvsp[0], 1); // 检查类型是否匹配
		yyval = genNode("arithexp", 0); 
		addChild(yyval, yyvsp[-2]);
		addChild(yyval, yyvsp[-1]);
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, yyvsp[-2]->type);

		// 中间代码生成
		// $$->code = $3->code || $1->code || "$1->name * $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[0]->code);
		strcat(yyval->code, yyvsp[-2]->code);

		char newcode[25];
		sprintf(newcode, "_t%d = ", yyval->t_id);
		if(yyvsp[-2]->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, yyvsp[-2]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[-2]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " * ");
		if(yyvsp[0]->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, yyvsp[0]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[0]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat(yyval->code, newcode);
	}
#line 1955 "y.tab.c"
    break;

  case 28:
#line 458 "ga.y"
                                      {
		checkType(yyvsp[-2], yyvsp[0], 1); // 检查类型是否匹配
		yyval = genNode("arithexp", 0); 
		addChild(yyval, yyvsp[-2]);
		addChild(yyval, yyvsp[-1]);
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, yyvsp[-2]->type);

		// 中间代码生成
		// $$->code = $3->code || $1->code || "$1->name / $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[0]->code);
		strcat(yyval->code, yyvsp[-2]->code);

		char newcode[25];
		sprintf(newcode, "_t%d = ", yyval->t_id);
		if(yyvsp[-2]->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, yyvsp[-2]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[-2]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " / ");
		if(yyvsp[0]->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, yyvsp[0]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[0]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat(yyval->code, newcode);
	}
#line 1995 "y.tab.c"
    break;

  case 29:
#line 494 "ga.y"
              {
		yyval = genNode(yyvsp[0]->content, 0); 
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = "t1 = 1.23"
		yyval->t_id = newTempID();
		sprintf(yyval->code, "_t%d = %s\n", yyval->t_id, yyval->content);
	}
#line 2010 "y.tab.c"
    break;

  case 30:
#line 504 "ga.y"
                 {
		yyval = genNode("boolexp", 0); 
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = $1->code || "$$->name = $1->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[0]->code);
		char newcode[25];
		sprintf(newcode, "_t%d = _t%d\n", yyval->t_id , yyvsp[0]->t_id);
		strcat(yyval->code, newcode);
	}
#line 2028 "y.tab.c"
    break;

  case 31:
#line 517 "ga.y"
                      {
		yyval = genNode("boolexp", 0); 
		addChild(yyval, yyvsp[-2]); addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = $2->code || "$$->name = $2->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[-1]->code);
		char newcode[25];
		sprintf(newcode, "_t%d = _t%d\n", yyval->t_id , yyvsp[-1]->t_id);
		strcat(yyval->code, newcode);
	}
#line 2046 "y.tab.c"
    break;

  case 32:
#line 530 "ga.y"
                  {
		yyval = genNode("boolexp", 0); 
		addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = $2->code || "$$->name = not $2->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[0]->code);
		char newcode[25];
		sprintf(newcode, "_t%d = not _t%d\n", yyval->t_id , yyvsp[0]->t_id);
		strcat(yyval->code, newcode);

	}
#line 2065 "y.tab.c"
    break;

  case 33:
#line 544 "ga.y"
                          {
		yyval = genNode("boolexp", 0); 
		addChild(yyval, yyvsp[-2]); addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name AND $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[-2]->code);
		strcat(yyval->code, yyvsp[0]->code);
		char newcode[25];
		sprintf(newcode, "_t%d = _t%d AND _t%d", yyval->t_id, yyvsp[-2]->t_id, yyvsp[0]->t_id);
		strcat(yyval->code, newcode);
	}
#line 2084 "y.tab.c"
    break;

  case 34:
#line 558 "ga.y"
                         {
		yyval = genNode("boolexp", 0); 
		addChild(yyval, yyvsp[-2]); addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name OR $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[-2]->code);
		strcat(yyval->code, yyvsp[0]->code);
		char newcode[25];
		sprintf(newcode, "_t%d = _t%d OR _t%d", yyval->t_id, yyvsp[-2]->t_id, yyvsp[0]->t_id);
		strcat(yyval->code, newcode);
	}
#line 2103 "y.tab.c"
    break;

  case 35:
#line 573 "ga.y"
             {
		yyval = genNode(yyvsp[0]->content, 0); 
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_char);

		// 中间代码生成
		// $$->code = "t1 = 'a'"
		yyval->t_id = newTempID();
		sprintf(yyval->code, "_t%d = %s\n", yyval->t_id, yyval->content);
	}
#line 2118 "y.tab.c"
    break;

  case 36:
#line 583 "ga.y"
             {
		yyval = genNode(yyvsp[0]->content, 0); 
		addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_string);

		// 中间代码生成
		// $$->code = "t1 = "aa""
		yyval->t_id = newTempID();
		sprintf(yyval->code, "_t%d = %s\n", yyval->t_id, yyval->content);
	}
#line 2133 "y.tab.c"
    break;

  case 37:
#line 595 "ga.y"
                                      {
		yyval = genNode("comparison", 0); 
		addChild(yyval, yyvsp[-2]); addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name > $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[-2]->code);
		strcat(yyval->code, yyvsp[0]->code);
		char newcode[25];
		sprintf(newcode, "_t%d = ", yyval->t_id);
		if(yyvsp[-2]->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, yyvsp[-2]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[-2]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " > ");
		if(yyvsp[0]->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, yyvsp[0]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[0]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat(yyval->code, newcode);
	}
#line 2169 "y.tab.c"
    break;

  case 38:
#line 626 "ga.y"
                                      {
		yyval = genNode("comparison", 0); 
		addChild(yyval, yyvsp[-2]); addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name < $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[-2]->code);
		strcat(yyval->code, yyvsp[0]->code);
		char newcode[25];
		sprintf(newcode, "_t%d = ", yyval->t_id);
		if(yyvsp[-2]->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, yyvsp[-2]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[-2]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " < ");
		if(yyvsp[0]->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, yyvsp[0]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[0]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat(yyval->code, newcode);
		
	}
#line 2206 "y.tab.c"
    break;

  case 39:
#line 658 "ga.y"
                                      {
		yyval = genNode("comparison", 0); 
		addChild(yyval, yyvsp[-2]); addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name == $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[-2]->code);
		strcat(yyval->code, yyvsp[0]->code);
		char newcode[25];
		sprintf(newcode, "_t%d = ", yyval->t_id);
		if(yyvsp[-2]->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, yyvsp[-2]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[-2]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " == ");
		if(yyvsp[0]->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, yyvsp[0]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[0]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat(yyval->code, newcode);
		
	}
#line 2243 "y.tab.c"
    break;

  case 40:
#line 690 "ga.y"
                                     {
		yyval = genNode("comparison", 0); 
		addChild(yyval, yyvsp[-2]); addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name >= $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[-2]->code);
		strcat(yyval->code, yyvsp[0]->code);
		char newcode[25];
		sprintf(newcode, "_t%d = ", yyval->t_id);
		if(yyvsp[-2]->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, yyvsp[-2]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[-2]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " >= ");
		if(yyvsp[0]->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, yyvsp[0]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[0]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat(yyval->code, newcode);
		
	}
#line 2280 "y.tab.c"
    break;

  case 41:
#line 722 "ga.y"
                                     {
		yyval = genNode("comparison", 0); 
		addChild(yyval, yyvsp[-2]); addChild(yyval, yyvsp[-1]); addChild(yyval, yyvsp[0]);
		setNodeType(yyval, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name <= $3->name" 
		yyval->t_id = newTempID();
		strcpy(yyval->code, yyvsp[-2]->code);
		strcat(yyval->code, yyvsp[0]->code);
		char newcode[25];
		sprintf(newcode, "_t%d = ", yyval->t_id);
		if(yyvsp[-2]->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, yyvsp[-2]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[-2]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " <= ");
		if(yyvsp[0]->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, yyvsp[0]->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", yyvsp[0]->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat(yyval->code, newcode);
		
	}
#line 2317 "y.tab.c"
    break;


#line 2321 "y.tab.c"

      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */
  {
    const int yylhs = yyr1[yyn] - YYNTOKENS;
    const int yyi = yypgoto[yylhs] + *yyssp;
    yystate = (0 <= yyi && yyi <= YYLAST && yycheck[yyi] == *yyssp
               ? yytable[yyi]
               : yydefgoto[yylhs]);
  }

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYEMPTY : YYTRANSLATE (yychar);

  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
# define YYSYNTAX_ERROR yysyntax_error (&yymsg_alloc, &yymsg, \
                                        yyssp, yytoken)
      {
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = YYSYNTAX_ERROR;
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == 1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = YY_CAST (char *, YYSTACK_ALLOC (YY_CAST (YYSIZE_T, yymsg_alloc)));
            if (!yymsg)
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = 2;
              }
            else
              {
                yysyntax_error_status = YYSYNTAX_ERROR;
                yymsgp = yymsg;
              }
          }
        yyerror (yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:
  /* Pacify compilers when the user code never invokes YYERROR and the
     label yyerrorlab therefore never appears in user code.  */
  if (0)
    YYERROR;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYTERROR;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;


/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;


#if !defined yyoverflow || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif


/*-----------------------------------------------------.
| yyreturn -- parsing is finished, return the result.  |
`-----------------------------------------------------*/
yyreturn:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  yystos[+*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  return yyresult;
}
#line 755 "ga.y"


// 生成一个内容为 content 行数为 line 的空节点
Node* genNode(char* content, int line){
	Node* p = NULL;
	if ((p = malloc(sizeof(Node))) == NULL){
		yyerror("out of memory");
	}
	p->content = strdup(content);
	p->cnum = 0;
	p->line = line;
	p->id = id++;
	p->t_id = -1;
	p->next = -1;
	for(int i = 0; i < 10; i++){
		p->children[i] = NULL;
	}
	return p;
}

// 为一个节点 p 添加一个子节点 child
void addChild(Node* p, Node* child){
	p->children[p->cnum] = child;
	p->cnum++;
}

// 递归释放以该节点为根的子树的空间
void freeNode(Node* p){
	if(p == NULL){
		return;
	}
	for(int i = 0; i < p->cnum; i++){
		freeNode(p->children[i]);
	}
	free(p->content);
	free(p);
}

// 可视化生成树
void showNode(Node* p, int d, int i){
	if(p == NULL){
		return;
	}
	for(int i = 0; i < d; i++){
		printf("   ");
	}
	
	printf("(%d,%d) %s [next: %d] \n", d, i, p->content, p->next);
	// printf("(%d,%d) %s [type: %s] \n", d, i, p->content, type_string[(int)p->type]);
	for(int i = 0; i < p->cnum; i++){
		showNode(p->children[i], d+1, i+1);	
	}
}

// 设置节点类型
void setNodeType(Node*p, SymbolType type){
	p->type = type;
}


// 根据 变量声明部分 declaration 生成符号表
// Node *declaration 是以一行变量声明生成的子树
// 其左节点为变量类型，右节点为ID构成的子树
int updateSymbolTable(Node* declaration){
    if(declaration == NULL || declaration->children[0] == NULL || declaration->cnum == 0) {
        return 0;
    }
    enum SymbolType type;
    char typeSpecifier = declaration->children[0]->content[0]; // 类型的首字母
    switch (typeSpecifier) {
        case 'i':
            type = st_int;
            break;
        case 'f':
            type = st_float;
            break;
        case 'b':
            type = st_bool;
            break;
        case 'c':
            type = st_char;
            break;
        case 's':
            type = st_string;
            break;
    }
    appendSymbol(type, declaration->children[1]);
    return 1;
} 

// 更新符号表的同时更新节点的类型
void appendSymbol(enum SymbolType type, Node* node){
    if(node->line == 0) { // 处理非终结符号 varlist
        for(int i = 0; i < node->cnum; i++){
            appendSymbol(type, node->children[i]);
        }
    }
    else { // 处理终结符号 ID
        int len1 = strlen(node->content);
        for(int j = 0; j < symbolNum; j++){
            int len2 = strlen(symbolTable[j].id);
            if(len1 == len2 && memcmp(symbolTable[j].id, node->content, len1) == 0) {
                // 检测到符号表已经出现同名 ID
                fprintf(stderr, "Error at Line %02d: 重复定义变量 %s\n", node->line, node->content);
                exit(1);
            }    
        }
        symbolTable[symbolNum].type = type;
		node->type = type;
		node->t_id = -1;
        memcpy(symbolTable[symbolNum].id, node->content, len1);
        symbolNum++;
    }
}

// 符号表可视化
void showSymbolTable(){
    printf("\nSymbol Table \n");
    printf("      TYPE       ID        VAL\n");
    
    for(int i = 0; i < symbolNum; i++){
        printf("%3d %6s ", i, type_string[(int)symbolTable[i].type]);
        printf("%8s %10s\n", symbolTable[i].id, symbolTable[i].value);
    }
}

// 检查 ID 是否出现在符号表中，若不出现则报错
void checkID(Node* node) {
	int len1 = strlen(node->content);
	for(int j = 0; j < symbolNum; j++){
		int len2 = strlen(symbolTable[j].id);
		if(len1 == len2 && memcmp(symbolTable[j].id, node->content, len1) == 0) {
			// 在符号表中检测到了该 ID 名
			node->type = symbolTable[j].type;
			return;
		}    
	}
	// ID 不存在，出错
	fprintf(stderr, "Error at Line %02d: 使用未定义变量 %s\n", node->line, node->content);
    exit(1);
}


// 检查两个节点的类型是否相同，不同则出错
void checkType(Node *node1, Node* node2, int level) {
	if(level == 2){ // 针对赋值语句
		if(node1->type == st_float && node2->type == st_int){
			return;
		}
	}
	
	if(level == 1){ // 针对算术运算
		if((node1->type == st_float && node2->type == st_int) || (node1->type == st_int && node2->type == st_float))
		return;
	}
	
	if(node1->type != node2->type){
		fprintf(stderr, "Error at Line %02d: 类型不匹配 %s, %s\n", node1->line, node1->content, node2->content);
		exit(1);
	}
}

void getTreeCode(Node* p, int end){
	if(p == NULL){
		return;
	}

	char node_info[120];
	char node_name[100];
	if(p->type == st_null){
		sprintf(node_name, "%s",p->content);
	}
	else{
		sprintf(node_name, "%s(%s)",p->content, type_string[(int)p->type]);
	}
	
	sprintf(node_info, "id%d[label=\"%s\"]\n", p->id, node_name);
	strcat(map, node_info);
	
	
	for(int i = 0; i < p->cnum; i++){
		getTreeCode(p->children[i], 0);	
		char line_info[120];
		sprintf(line_info, "id%d->id%d\n", p->id, p->children[i]->id);
		strcat(map, line_info);
	}

	if(end == 1){
		char end_sign[5] = "}\n";
		strcat(map, end_sign);
		
		FILE* fp = fopen("./treemap.txt", "w");
		fputs(map, fp);
		fclose(fp);
		char header[150] = "digraph demo{\nnode [shape=box, style=\"rounded\", color=\"black\", fontname=\"Microsoft YaHei\"];\nedge [fontname=\"Microsoft YaHei\"];\n";
		strcpy(map, header);
	}
}

int newLabel(){
	return label_id++;
}

int newTempID(){
	return temp_id++;
}

// 因为我们有节点的全局ID 中间代码中每一个为定义next标号可以先用全局ID给他标记下来
// 这样对于一个中间代码文本中，我们可以找到他，并识别他的原本在语法树中的节点。
// 我们遍历一遍树，将必要的next = $$->next自顶向下更新。
// 同时我们每更新一个节点，就去中间代码串中寻找他的位置，并修改成我们新赋值的next值。

void UpdateNext(Node* root, char code[]){
	for(int i = 0; i < root->cnum; i++){
		Node* child = root->children[i];
		if(child->next == -1){
			child->next = root->next;
			char nullnext[25];
			char realnext[25];
			sprintf(nullnext, "__Label %03d__", child->id);
			sprintf(realnext, "Label %03d    ", root->next);
			// printf("%s,%s\n",nullnext, realnext);
			while(1){
				char* h = strstr(code, nullnext);
				if(h == NULL){
					break;
				}
				for(int i = 0; i < strlen(realnext); i++){
					h[i] = realnext[i];
				}
			}
		}
		UpdateNext(child, code);
	}
}




int main(void) {
	char infile[100];
	printf("Input File: \n");
	scanf("%s", infile);
	yyin = fopen(infile, "r");
	if(yyin == NULL){
		printf("Error: 文件无法打开\n");
		exit(1);
	}
	
	// printf("Line 01: ");

	yyparse();
	
	
	// 输出语法分析树
	// showNode(root, 0, 1); 

	// 输出符号表
	showSymbolTable();

	// 生成可视化语法树
	// 成在`treemap.txt`，然后用python运行`tree.py`即可生成可视化语法树`tree.png`。
	getTreeCode(root, 1);

	// 中间代码生成器：输出中间代码
	printf("\nCode:\n%s", root->code);

	// 释放内存
	freeNode(root);

	return 0;
}
