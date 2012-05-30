from london.urls.defining import patterns

url_patterns = patterns('comments.views',
        (r'^post/$', 'post_comment', {}, 'post_comment'),
)