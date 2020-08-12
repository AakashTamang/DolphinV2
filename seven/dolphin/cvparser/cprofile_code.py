import cProfile, pstats, io

# a decorator that uses cProfile to profile a function
def profile(function):

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = function(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        # print(s.getvalue())
        with open(f'cprofile reports/{function.__name__}.txt','w') as f:
            f.write(s.getvalue())
        return retval

    return inner


'''
To be used when not using for function

pr = cProfile.Profile()
pr.enable()
# line of code
pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
# print (s.getvalue())
with open('profile_report.txt','w') as f:
    f.write(s.getvalue())
'''