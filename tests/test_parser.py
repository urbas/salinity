from salinity import parser


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
