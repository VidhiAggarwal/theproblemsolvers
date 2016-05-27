         
                function upvote() {
                    var post_id = {{ i.id }}
                    $.post({
                        url: 'postIssue:upvote',
                        data: {id: post_id },
                        type: 'GET',
                        success: function(response) {
                            alert(response);
                        }
                    });
                }
      