from london.dispatch import Signal

# This signal is useful for customizing and adding single fields to the comment
post_comment = Signal(required=('comment','request'))
