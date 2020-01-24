import numpy as np
import re
from scipy.spatial import distance


regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def check_email(email):
    if re.search(regex, email):
        return True
    else:
        return False


def ohe(email):
    if check_email(email):
        alph = 'abcdefghijklmnopqrstuvwxyz1234567890@._'
        x_one_hot = []
        for i in list(alph):
            if i in list(email):
                x_one_hot.append(1)
            else:
                x_one_hot.append(0)
        return np.array(x_one_hot)
    else:
        print('Wrong email format!')


def main():
    print('Enter first email: ')
    email1 = ohe(input().lower())
    print('Enter second email: ')
    email2 = ohe(input().lower())
    print('Emails are similar to ', round(100*(1-distance.cosine(email1, email2)),2), '%')


if __name__ == '__main__':
    main()
