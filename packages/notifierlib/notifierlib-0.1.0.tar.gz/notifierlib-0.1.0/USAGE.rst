=====
Usage
=====

To use notifierlib in a project:

.. code-block:: python

    from notifierlib.channels import Email
    from notifierlib.channels import Stdout
    from notifierlib import Notifier, Group

    # import logging and set it to debug so we can see what is going on
    import logging
    logging.basicConfig(level=logging.DEBUG)

    # instantiate the main object
    notifier=Notifier()


    # instantiate channels for email and stdout
    # the first argument is the name of the channel since we can have many
    # channels of the same type if we only give them distinct names
    email=Email('email',
                sender='sender.email@gmail.com',
                recipient='recipient.email@gmail.com',
                smtp_address='smtp.domain.com',
                username='smtp_username',
                password='smtp_password',
                tls=True,
                ssl=False,
                port=587)

    stdout=Stdout('stdout')

    # register the channels to notifier
    notifier.register(stdout, email)

    # or just one by one
    notifier.register(stdout, email)

    # this attribute shows us the names of the registered channels
    notifier.channels
     # >>> ['stdout', 'email']

     # from here on we have access to a "broadcast" method than will propagate
     # the supplied arguments to all registered channels
    notifier.broadcast(subject='yay!!', message='this is a message')

    # this is the debug output of the above
    DEBUG:notifierlib.Group:Sending notification using channel: stdout with args:{'message': 'this is a message', 'subject': 'yay!!'}
    DEBUG:notifierlib.Group:Sending notification using channel: email with args:{'message': 'this is a message', 'subject': 'yay!!'}
    DEBUG:emaillib.emaillib:Trying to connect via SMTP
    DEBUG:notifierlib.Group:Waiting for results
    Subject :yay!!
    Message :this is a message
    ()
    INFO:emaillib.emaillib:Got smtp connection
    INFO:emaillib.emaillib:Logging in
    DEBUG:emaillib.emaillib:Done
    DEBUG:notifierlib.Group:Result of notification: [{'stdout': True}, {'email': True}]

    # we can fine tune the channel collections by creating groups
    # again the first argument is the group name and all other arguments should
    # be of type channel
    email_group=Group('email', email)

    print(email_group.name)
    >>> 'email'

    # we add the group to the notifier
    notifier.add_group(email_group)

    # and from here on we have a method with the name of the group that can accept
    # our arguments and it will propagate them its the registered channels
    notifier.email(subject='test',message='as')

    DEBUG:notifierlib.Group:Sending notification using channel: email with args:{'message': 'as', 'subject': 'test'}
    DEBUG:notifierlib.Group:Waiting for results
    DEBUG:emaillib.emaillib:Trying to connect via SMTP
    INFO:emaillib.emaillib:Got smtp connection
    INFO:emaillib.emaillib:Logging in
    DEBUG:emaillib.emaillib:Done
    DEBUG:notifierlib.Group:Result of notification: [{'email': True}]

    # and we can remove the method by removing the group from the notifier
    notifier.remove_group(email_group)
    >>>True

    # another group example
    debug_group=Group('debug', stdout)
    notifier.add_group(debug_group)
    notifier.debug(subject='test')
    Subject :test
    Message :None
    ()
    DEBUG:notifierlib.Group:Sending notification using channel: stdout with args:{'subject': 'test'}
    DEBUG:notifierlib.Group:Waiting for results
    DEBUG:notifierlib.Group:Result of notification: [{'stdout': True}]
