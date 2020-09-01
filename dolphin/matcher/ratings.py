## This part is done through scoring api
# employerPrefs = {
#  'Job_1':  ['Badal', 'Jit', 'Aakash', 'Sunil', 'Sagar', 'Nitesh', 'Sandesh', 'Sajjan', 'Shushant', 'Sujan'],
#  'Job_2':  ['Sagar', 'Nitesh', 'Sujan', 'Aakash', 'Sajjan', 'Jit', 'Badal', 'Sunil', 'Shushant', 'Sandesh'],
#  'Job_3':  ['Sujan', 'Jit', 'Sandesh', 'Sunil', 'Nitesh', 'Sajjan', 'Aakash', 'Shushant', 'Badal', 'Sagar'],
#  'Job_4':  ['Sujan', 'Nitesh', 'Sagar', 'Jit', 'Badal', 'Shushant', 'Sandesh', 'Sajjan', 'Sunil', 'Aakash'],
#  'Job_5':  ['Sunil', 'Nitesh', 'Badal', 'Sajjan', 'Shushant', 'Sujan', 'Aakash', 'Sagar', 'Sandesh', 'Jit'],
#  'Job_6':  ['Shushant', 'Sagar', 'Sujan', 'Aakash', 'Nitesh', 'Jit', 'Sajjan', 'Sandesh', 'Badal', 'Sunil'],
#  'Job_7':  ['Sujan', 'Nitesh', 'Shushant', 'Badal', 'Sandesh', 'Aakash', 'Jit', 'Sajjan', 'Sagar', 'Sunil'],
#  'Job_8':  ['Sagar', 'Shushant', 'Aakash', 'Sunil', 'Sajjan', 'Sujan', 'Jit', 'Badal', 'Sandesh', 'Nitesh'],
#  'Job_9':  ['Sandesh', 'Aakash', 'Sajjan', 'Shushant', 'Jit', 'Nitesh', 'Sujan', 'Badal', 'Sagar', 'Sunil'],
#  'Job_10': ['Sajjan', 'Sujan', 'Aakash', 'Sunil', 'Nitesh', 'Badal', 'Shushant', 'Sandesh', 'Sagar', 'Jit']}

## This part is manually given by the candidates
# candidatePrefs = {
#  'Aakash':  ['Job_10', 'Job_3', 'Job_2', 'Job_7', 'Job_8', 'Job_4', 'Job_5', 'Job_1', 'Job_6', 'Job_9'],
#  'Badal':  ['Job_8', 'Job_2', 'Job_4', 'Job_5', 'Job_10', 'Job_6', 'Job_7', 'Job_9', 'Job_3', 'Job_1'],
#  'Jit':  ['Job_6', 'Job_7', 'Job_9', 'Job_8', 'Job_3', 'Job_1', 'Job_10', 'Job_5', 'Job_2', 'Job_4'],
#  'Nitesh':  ['Job_3', 'Job_4', 'Job_10', 'Job_1', 'Job_7', 'Job_5', 'Job_2', 'Job_9', 'Job_8', 'Job_6'],
#  'Sagar': ['Job_5', 'Job_3', 'Job_6', 'Job_7', 'Job_8', 'Job_1', 'Job_4', 'Job_9', 'Job_2', 'Job_10'],
#  'Sajjan':  ['Job_6', 'Job_7', 'Job_2', 'Job_10', 'Job_5', 'Job_1', 'Job_8', 'Job_9', 'Job_3', 'Job_4'],
#  'Sandesh':  ['Job_9', 'Job_4', 'Job_5', 'Job_7', 'Job_6', 'Job_3', 'Job_2', 'Job_8', 'Job_10', 'Job_1'],
#  'Shushant': ['Job_10', 'Job_6', 'Job_9', 'Job_5', 'Job_4', 'Job_2', 'Job_8', 'Job_7', 'Job_1', 'Job_3'],
#  'Sujan':  ['Job_6', 'Job_10', 'Job_3', 'Job_5', 'Job_8', 'Job_7', 'Job_1', 'Job_9', 'Job_2', 'Job_4'],
#  'Sunil':  ['Job_3', 'Job_5', 'Job_4', 'Job_10', 'Job_6', 'Job_7', 'Job_2', 'Job_9', 'Job_1', 'Job_8']}

## Scores are given within the scale of 100

## Employers giving score to candidates
## Scores are calculated from scoring api
## "42" = job__id
## "152":5.0 = "user_id:score given by jd"
oneJD_MultipleRes_Score = {
    "42": {
        "152": 5.0,
        "153": 62.5342799316753,
        "154": 50.93863099813461,
        "155": 50.306867212057114
    },
    "43":{
        "152": 10.0,
        "153": 77.5342799316753,
        "154": 80.93863099813461,
        "155": 55.306867212057114
    },
    "44":{
        "152": 30.0,
        "153": 32.5342799316753,
        "154": 45.93863099813461,
        "155": 88.306867212057114
    },
    "45":{
        "152": 15.0,
        "153": 22.5342799316753,
        "154": 60.93863099813461,
        "155": 40.306867212057114
    }
}

## "152" = user_id
## "42":55.0 = "job_id":score given by user
oneRes_MultipleJD_Score = {
    "152":{
        "42": 55.0,
        "43": 60.0,
        "44": 11.0,
        "45": 89.0
    },
    "153":{
        "42": 20.0,
        "43": 50.0,
        "44": 71.0,
        "45": 59.0
    },
    "154":{
        "42": 85.0,
        "43": 10.0,
        "44": 51.0,
        "45": 69.0
    },
    "155":{
        "42": 65.0,
        "43": 30.0,
        "44": 61.0,
        "45": 39.0
    }
}