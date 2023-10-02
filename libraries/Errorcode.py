from kivy.metrics import dp
from datetime import datetime

dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

row_data = [
        [
            dt,
            '0001',
            ["alert", "No Signal"],
            "Astrid: NE shared managed",
            "Medium",
        ],
        [
            dt,
            '0102',
            ["alert-circle",[1, 0, 0, 1],"Offline"],
            "Cosmo: prod shared ares",
            "Huge",
        ],
        [
            dt,
            '0002',
            ["checkbox-marked-circle",[39 / 256, 174 / 256, 96 / 256, 1],"Online"],
            "Phoenix: prod shared lyra-lists",
            "Minor",
        ],
        [
            dt,
            '0123',
            "Online",
            "Sirius: NW prod shared locations",
            "Negligible",
        ],
        [
            dt,
            '0304',
            "Online",
            "asdasdas ",
            "Negligible",
        ],
        [
            dt,
            '0202',
            "Online",
            "Sirius: prod independent account",
            "Negligible",
        ],
        [
            dt,
            '0018',
            "Online",
            "Sirius: prod independent account",
            "Negligible",
        ],
]

column_data = [
    [
        "Date",
        dp(60),
    ],
    [
        "Error Code",
        dp(30),
    ],
    [
        "Signal",
        dp(30),
    ],
    [
        "Error Message",
        dp(50),
    ],
    [
        "Resolve",
        dp(50),
    ],

]

row_data1 = [
        [
            dt,
            '0001',
            ["alert", "No Signal"],
            "321",
            "Medium",
        ],
        [
            dt,
            '0102',
            ["alert-circle",[1, 0, 0, 1],"Offline"],
            "123",
            "Huge",
        ],
        [
            dt,
            '1212345',
            ["checkbox-marked-circle",[39 / 256, 174 / 256, 96 / 256, 1],"Online"],
            "456",
            "Minor",
        ],
        [
            dt,
            '345',
            "Online",
            "Sirius: NW prod shared locations",
            "Negligible",
        ],
        [
            dt,
            '0304',
            "Online",
            "asdasdas ",
            "Negligible",
        ],
        [
            dt,
            '0202',
            "Online",
            "Sirius: prod independent account",
            "Negligible",
        ],
        [
            dt,
            '0018',
            "Online",
            "Sirius: prod independent account",
            "Negligible",
        ],
]

column_data1 = [
    [
        "Date",
        dp(60),
    ],
    [
        "Error Code",
        dp(30),
    ],
    [
        "Signal",
        dp(30),
        "center",
    ],
    [
        "Error Message",
        dp(50),
    ],
    [
        "Resolve",
        dp(50),
    ],

]