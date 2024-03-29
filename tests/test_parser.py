from os.path import dirname, join
from salinity import parser

SAMPLE_OUTPUT = """local:
  Name: /etc/salt/grains - Function: file.managed - Result: Clean Started: - 10:16:58.807965 Duration: 65.815 ms
----------
          ID: /etc/salt/grains
    Function: file.managed
      Result: True
     Comment: File /etc/salt/grains updated
     Started: 10:16:17.259542
    Duration: 51.236 ms
     Changes:
              ----------
              diff:
                  ---
                  +++
                  @@ -1,3 +1 @@
                   roles: []
                  -foo
                  -bar
  Name: [ -f /swapfile ] || fallocate -l 4096M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
swapon -a
 - Function: cmd.run - Result: Clean Started: - 10:17:20.639763 Duration: 480.786 ms
  Name: localhost - Function: host.present - Result: Clean Started: - 10:16:59.791990 Duration: 1.721 ms
Summary for local
--------------
Succeeded: 142 (changed=1)
Failed:      0
--------------
Total states run:     142
Total run time:   114.396 s"""


def test_parse():
    parsed_output = parser.parse(SAMPLE_OUTPUT)
    assert (
        [
            {
                "name": "/etc/salt/grains",
                "function": "file.managed",
                "result": "Clean",
                "duration_ms": 65.815,
            },
            {
                "id": "/etc/salt/grains",
                "name": "/etc/salt/grains",
                "function": "file.managed",
                "result": "True",
                "duration_ms": 51.236,
            },
            {
                "name": """[ -f /swapfile ] || fallocate -l 4096M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
swapon -a""",
                "function": "cmd.run",
                "result": "Clean",
                "duration_ms": 480.786,
            },
            {
                "name": "localhost",
                "function": "host.present",
                "result": "Clean",
                "duration_ms": 1.721,
            },
        ]
        == parsed_output["changes"]
    )


def test_extract_changes():
    assert [
        "  Name: /etc/salt/grains - Function: file.managed - Result: Clean Started: - 10:16:58.807965 "
        "Duration: 65.815 ms",
        "----------",
        "          ID: /etc/salt/grains",
        "    Function: file.managed",
        "      Result: True",
        "     Comment: File /etc/salt/grains updated",
        "     Started: 10:16:17.259542",
        "    Duration: 51.236 ms",
        "     Changes:",
        "              ----------",
        "              diff:",
        "                  ---",
        "                  +++",
        "                  @@ -1,3 +1 @@",
        "                   roles: []",
        "                  -foo",
        "                  -bar",
        "  Name: [ -f /swapfile ] || fallocate -l 4096M /swapfile",
        "chmod 0600 /swapfile",
        "mkswap /swapfile",
        "swapon -a",
        " - Function: cmd.run - Result: Clean Started: - 10:17:20.639763 Duration: 480.786 ms",
        "  Name: localhost - Function: host.present - Result: Clean Started: - 10:16:59.791990 Duration: 1.721 ms",
    ] == parser.extract_changes(SAMPLE_OUTPUT.splitlines())


def test_multiple_clean_entries():
    assert [
        {
            "name": "/etc/salt/grains",
            "function": "file.managed",
            "result": "Clean",
            "duration_ms": 65.815,
        },
        {
            "name": "localhost",
            "function": "host.present",
            "result": "Clean",
            "duration_ms": 1.721,
        },
    ] == parser.parse_changes_fmt(
        """  Name: /etc/salt/grains - Function: file.managed - Result: Clean Started: - 10:16:58.807965 Duration: 65.815 ms
  Name: localhost - Function: host.present - Result: Clean Started: - 10:16:59.791990 Duration: 1.721 ms""".splitlines()
    )


def test_multiple_mixed_entries():
    assert (
        [
            {
                "name": "/etc/salt/grains",
                "function": "file.managed",
                "result": "Clean",
                "duration_ms": 65.815,
            },
            {
                "id": "/etc/salt/grains",
                "name": "/etc/salt/grains",
                "function": "file.managed",
                "result": "True",
                "duration_ms": 51.236,
            },
            {
                "name": """[ -f /swapfile ] || fallocate -l 4096M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
swapon -a""",
                "function": "cmd.run",
                "result": "Clean",
                "duration_ms": 480.786,
            },
            {
                "name": "localhost",
                "function": "host.present",
                "result": "Clean",
                "duration_ms": 1.721,
            },
        ]
        == parser.parse_changes_fmt(
            """  Name: /etc/salt/grains - Function: file.managed - Result: Clean Started: - 10:16:58.807965 Duration: 65.815 ms
----------
          ID: /etc/salt/grains
    Function: file.managed
      Result: True
     Comment: File /etc/salt/grains updated
     Started: 10:16:17.259542
    Duration: 51.236 ms
     Changes:
              ----------
              diff:
                  ---
                  +++
                  @@ -1,3 +1 @@
                   roles: []
                  -foo
                  -bar
  Name: [ -f /swapfile ] || fallocate -l 4096M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
swapon -a
 - Function: cmd.run - Result: Clean Started: - 10:17:20.639763 Duration: 480.786 ms
  Name: localhost - Function: host.present - Result: Clean Started: - 10:16:59.791990 Duration: 1.721 ms""".splitlines()
        )
    )


def test_single_clean_entry():
    assert {
        "name": "/etc/salt/grains",
        "function": "file.managed",
        "result": "Clean",
        "duration_ms": 65.815,
    } == parser.parse_clean_entry(
        "  Name: /etc/salt/grains - Function: file.managed - Result: Clean Started: - 10:16:58.807965 "
        "Duration: 65.815 ms"
    )


def test_single_clean_multiline_entry():
    assert (
        {
            "name": """[ -f /swapfile ] || fallocate -l 4096M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
swapon -a""",
            "function": "cmd.run",
            "result": "Clean",
            "duration_ms": 480.786,
        }
        == parser.parse_clean_entry(
            """  Name: [ -f /swapfile ] || fallocate -l 4096M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
swapon -a
 - Function: cmd.run - Result: Clean Started: - 10:17:20.639763 Duration: 480.786 ms"""
        )
    )


def test_single_changed_entry():
    assert {
        "id": "/etc/salt/grains",
        "name": "/etc/salt/grains",
        "function": "file.managed",
        "result": "True",
        "duration_ms": 51.236,
    } == parser.parse_changed_entry(
        """----------
          ID: /etc/salt/grains
    Function: file.managed
      Result: True
     Comment: File /etc/salt/grains updated
     Started: 10:16:17.259542
    Duration: 51.236 ms
     Changes:
              ----------
              diff:
                  ---
                  +++
                  @@ -1,3 +1 @@
                   roles: []
                  -foo
                  -bar"""
    )


def test_changed_entry_name_override():
    assert {
        "id": "pyenv-installer.installed",
        "name": "/usr/bin/pyenv-installer",
        "function": "file.managed",
        "result": "True",
        "duration_ms": 15.716,
    } == parser.parse_changed_entry(
        """----------
          ID: pyenv-installer.installed
    Function: file.managed
        Name: /usr/bin/pyenv-installer
      Result: True
     Comment: File /usr/bin/pyenv-installer updated
     Started: 21:17:57.174034
    Duration: 15.716 ms
     Changes:
              ----------
              foobar"""
    )


def test_changes_highstate_sample_1():
    assert [
        {
            "name": "packages.installed",
            "function": "pkg.installed",
            "result": "Clean",
            "duration_ms": 89.726,
        },
        {
            "id": "pyenv-installer.installed",
            "name": "/usr/bin/pyenv-installer",
            "function": "file.managed",
            "result": "True",
            "duration_ms": 15.716,
        },
        {
            "name": "/usr/bin/pyenv",
            "function": "file.symlink",
            "result": "Clean",
            "duration_ms": 2.893,
        },
        {
            "name": "service.systemctl_reload",
            "function": "module.run",
            "result": "Clean",
            "duration_ms": 0.027,
        },
    ] == parser.parse(load_sample("changes-highstate-1.out"))["changes"]


def load_sample(sample_name):
    with open(join(dirname(__file__), "samples", sample_name)) as sample_file:
        return sample_file.read()
