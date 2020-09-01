from ratings import oneJD_MultipleRes_Score, oneRes_MultipleJD_Score
from match import matcher

hiredobj = matcher(oneJD_MultipleRes_Score, oneRes_MultipleJD_Score)
hired = hiredobj.matchmaker()

print('\nBest Match between candidate and companies:')
print('  ' + ',\n  '.join('%s is hired by %s' % match
                        for match in sorted(hired.items())))