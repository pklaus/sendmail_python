
# Example Script to Send E-Mails with Python3

### CLI Signature

    $ ./sendmail.py --help
    usage: sendmail.py [-h] --subject SUBJECT --from FROM --to TO --configfile
                       CONFIGFILE [--configsection CONFIGSECTION]
                       MAILBODY [ATTACHMENT [ATTACHMENT ...]]
    
    Send an email. With Python.
    
    positional arguments:
      MAILBODY              A text file containing the mail body itself
      ATTACHMENT            Optional files to attach
    
    optional arguments:
      -h, --help            show this help message and exit
      --subject SUBJECT
      --from FROM
      --to TO
      --configfile CONFIGFILE
                            The .ini file with the mailserver credentials
      --configsection CONFIGSECTION
                            The mail server section to choose in the configfile.

### Resources

* [Python documentation: `email` Examples](https://docs.python.org/3/library/email.examples.html)

