// 서버로부터 메시지를 가져오는 함수
function fetchMessages() {
    var getMessagesUrl = $('.container').data('get-messages-url');
    
    $.ajax({
        url: getMessagesUrl,
        type: 'GET',
        success: function(response) {
            $('#chat-log').empty();
            response.messages.forEach(function(message) {
                var messageHtml = `
                    <div class="message-container">
                        <div class="message-user">${message.user}:</div>
                        <div class="message-content">${message.content}</div>
                        <div class="message-timestamp">${message.timestamp}</div>
                    </div>`;
                $('#chat-log').append(messageHtml);
            });
            $('#chat-log').scrollTop($('#chat-log')[0].scrollHeight);
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}

function sendMessage() {
    var messageInput = $('#chat-message-input').val();
    if (messageInput.trim() !== '') {
        var sendMessageUrl = $('.container').data('send-message-url');
        var csrftoken = getCookie('csrftoken');
        
        $.ajax({
            url: sendMessageUrl,
            type: 'POST',
            data: {
                'content': messageInput,
                'csrfmiddlewaretoken': csrftoken
            },
            dataType: 'json',
            success: function(response) {
                $('#chat-message-input').val('');
                fetchMessages();
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    fetchMessages();
    
    $('#chat-message-submit').on('click', function() {
        sendMessage();
    });

    $('#chat-message-input').on('keypress', function(e) {
        if (e.which === 13) {
            sendMessage();
            return false;
        }
    });
});
