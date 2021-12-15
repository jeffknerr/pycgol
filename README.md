# pycgol
python fun with game of life program

I was originally trying to learn a little about 
[numpy](https://numpy.org/doc/stable/user/absolute_beginners.html),
so I wrote a [game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) 
program that uses numpy arrays. Along the way I also learned a little
about [click](https://click.palletsprojects.com/en/8.0.x/),
[pygame](https://www.pygame.org/news),
[python profiling](https://docs.python.org/3/library/profile.html),
and [python multiprocessing](https://docs.python.org/3/library/multiprocessing.html).



## running

I started with `pycgol.py`, then wrote a class (`gol.py`) to make
unit testing easier. You can run `app.py`, which uses instances
of the `GOL` class (defined in `gol.py`).

For small grids, display to terminal is fine:

```
# run 10x10 grid for 120 timesteps, display progress to terminal
./app.py --res 10 --nts 120 --term
```

![gol picture in terminal](gol-terminal.png)


For larger grids, you might want to display to pygame window:

```
# run 200x200 grid for 420 timesteps, display progress using pygame
./app.py --res 200 --nts 420 --pyg
```

![gol picture using pygame](gol-pygame.png)

See below for running the `multiprocessing` version.


## depends on

```
$ dpkg -l | grep pygame
ii  python3-pygame        1.9.6+dfsg-2build1

$ dpkg -l | grep python3-click
ii  python3-click         7.0-3

$ dpkg -l | grep numpy
ii  python3-numpy         1.17.4
```


## unit testing

Test the `count()` function in `utils.py`:

```
$ python3 test_utils.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

Test the `GOL` class and methods in `gol.py` (this tests for more
than just `count()` -- also tests that gol algorithm is actually
working):

```
$ python3 test_gol.py
.....
----------------------------------------------------------------------
Ran 5 tests in 0.070s

OK
```

## profiling

Even though this python implementation is not super fast, I still thought
it might be taking longer than it should. Below is an example of a profiling
run I did, that shows the old `count()` function I was using (in `utils.py`)
was taking a long time (77.5 seconds).

```
$ python3 -m cProfile -o output ./pycgol.py  --res 500 --nts 200
$ python3
Python 3.8.10 (default, Sep 28 2021, 16:10:42)
>>> import pstats
>>> from pstats import SortKey
>>> p = pstats.Stats('output')
>>> p.sort_stats(SortKey.CUMULATIVE).print_stats(10)
Mon Nov 29 12:12:40 2021    output

         51945224 function calls (51938635 primitive calls) in 111.858 seconds

   Ordered by: cumulative time
   List reduced from 2129 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    590/1    0.002    0.000  111.860  111.860 {built-in method builtins.exec}
        1    0.000    0.000  111.860  111.860 ./pycgol.py:3(<module>)
        1    0.000    0.000  111.664  111.664 /usr/lib/python3/dist-packages/click/core.py:762(__call__)
        1    0.000    0.000  111.664  111.664 /usr/lib/python3/dist-packages/click/core.py:658(main)
        1    0.000    0.000  111.663  111.663 /usr/lib/python3/dist-packages/click/core.py:950(invoke)
        1    0.001    0.001  111.663  111.663 /usr/lib/python3/dist-packages/click/core.py:518(invoke)
        1    0.036    0.036  111.662  111.662 ./pycgol.py:39(main)
      201   32.909    0.164  110.437    0.549 ./pycgol.py:82(update)
 50250000   77.502    0.000   77.502    0.000 /scratch/knerr/repos/pycgol/./utils.py:12(count)
      201    0.394    0.002    0.394    0.002 {built-in method pygame.display.flip}
```

## multiprocessing

Test runs for non-multiprocessing verion (`app.py`):

```
± $ for i in 1 2 3 4 5
for> do
for> echo ">>>>>>>>>>> $i"                                                                                        for> ./app.py --res 200 --pyg --nts 100
for> echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"                                                                     for> done
>>>>>>>>>>> 1
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
resolution: 200 x 200
 timesteps: 100
      time: 7.96 sec
     alive: 3641
      dead: 36359
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
>>>>>>>>>>> 2
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
resolution: 200 x 200
 timesteps: 100
      time: 7.98 sec
     alive: 3503
      dead: 36497
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
>>>>>>>>>>> 3
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
resolution: 200 x 200
 timesteps: 100
      time: 8.05 sec
     alive: 4123
      dead: 35877
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
>>>>>>>>>>> 4
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
resolution: 200 x 200
 timesteps: 100
      time: 8.28 sec
     alive: 3925
      dead: 36075
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
>>>>>>>>>>> 5
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
resolution: 200 x 200
 timesteps: 100
      time: 8.07 sec
     alive: 3540
      dead: 36460
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
```

Test runs for multiprocessing verion (`mpgol.py`):

```
$ for i in 1 2 3 4 5
do
echo ">>>>>>>>>>> $i"
./mpgrid.py --res 200 --nts 100
echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
done
>>>>>>>>>>> 1
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
resolution: 200 x 200
 timesteps: 100
processors: 2
      time: 4.22 sec
     alive: 3895
      dead: 36105
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
>>>>>>>>>>> 2
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
resolution: 200 x 200
 timesteps: 100
processors: 2
      time: 4.26 sec
     alive: 3765
      dead: 36235
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
>>>>>>>>>>> 3
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
resolution: 200 x 200
 timesteps: 100
processors: 2
      time: 4.14 sec
     alive: 4093
      dead: 35907
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
>>>>>>>>>>> 4
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
resolution: 200 x 200
 timesteps: 100
processors: 2
      time: 4.14 sec
     alive: 3774
      dead: 36226
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
>>>>>>>>>>> 5
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
resolution: 200 x 200
 timesteps: 100
processors: 2
      time: 4.12 sec
     alive: 3567
      dead: 36433
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
```

Seems to work (takes about half as long). I can halve the time again
by using `--procs 4`, but going to 8 doesn't decrease the total time
(sometimes even increases it a bit).

