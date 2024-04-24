# TODO: considering moving to ops_test for other forms too like school creation
# helps get rid of post man

import argparse
from argparse import Namespace
import requests


def get_nth_std(n: int, args: Namespace):
    roll = n
    student_id = int(args.grade) * 100 + roll
    data = {
        "form-0-school": args.ekey,
        "form-0-gradename": args.grade,
        "form-0-sectionname": args.section,
        "form-0-studentId": str(student_id),
        "form-0-roll_number": str(roll),
        "form-0-first_name": "Student",
        "form-0-middle_name": "",
        "form-0-last_name": f"{roll}",
        "form-0-gender": "MALE",
        "form-0-dob": "2023-12-06",
        "form-0-fathername": f"Father {roll}",
        "form-0-fatherphone": "1231231231",
        "form-0-mothername": f"Mother {roll}",
        "form-0-motherphone": "1231231231",
        "form-0-doj": "2024-04-01"
    }
    return data


def main():
    school_ekey = ""
    csrf_token = ""
    auth_token = ""
    session_id = ""
    host_url = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grade", default='1')
    parser.add_argument("-s", "--section", default='A')
    parser.add_argument("-n", type=int, default=3)
    parser.add_argument("-i", type=int, default=1)
    parser.add_argument("--ekey", default=school_ekey)
    parser.add_argument("--csrf-token", default=csrf_token)
    parser.add_argument("--auth-token", default=auth_token)
    parser.add_argument("--session-id", default=session_id)
    parser.add_argument("--host-url", default=host_url)
    args = parser.parse_args()

    for i, n_ in enumerate(range(args.n), start=args.i):
        print(f"Adding student {i}...")
        student = get_nth_std(i, args)
        resp = requests.post(
            f"{args.host_url}/school/{args.ekey}/{args.grade}/{args.section}/add-students",
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "origin": args.host_url,
                "cookie": f"csrftoken={args.csrf_token}; sessionid={args.session_id}; authtoken={args.auth_token};",
                "referer": args.host_url,
                "X-CSRFToken": args.csrf_token,
            },
            data={
                "csrfmiddlewaretoken": f"{args.csrf_token}",
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "1",
                "form-MIN_NUM_FORMS": "0",
                "form-MAX_NUM_FORMS": "1000",
                **student
            },
            allow_redirects=False,
        )
        print('resp status: ', resp.status_code)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
