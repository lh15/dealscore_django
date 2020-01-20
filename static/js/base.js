$(".upvote").click(function (event) {
    if (!is_authenticated) {
        return;
    }
    var linkID = event.target.parentNode.parentNode.parentNode.id;
    if(event.target.parentNode.classList.contains('voted')){
        $.post("/engine/unvote/" + linkID, {})
        .done(function (data) {
            $("#upvote_" + linkID).removeClass("voted");
        });
        return;
    }
    $.post("/engine/upvote/" + linkID, {})
        .done(function (data) {
            $("#downvote_" + linkID).removeClass("downvoted");
            $("#upvote_" + linkID).addClass("voted");
            $('#voted_modal').modal('show')
        });
});

$(".downvote").click(function (event) {
    if (!is_authenticated) {
        return;
    }
    var linkID = event.target.parentNode.parentNode.parentNode.id;
    if(event.target.parentNode.classList.contains('downvoted')){
        $.post("/engine/unvote/" + linkID, {})
        .done(function (data) {
            $("#downvote_" + linkID).removeClass("downvoted");
        });
        return;
    }

    $.post("/engine/downvote/" + linkID, {})
        .done(function (data) {
            $("#upvote_" + linkID).removeClass("voted");
            $("#downvote_" + linkID).addClass("downvoted");
            $('#voted_modal').modal('show')
        });
});

$(".deal_link").click(function (event) {
    var linkID = event.target.parentNode.parentNode.id;
    $.post("/engine/click_track/" + linkID, {})
        .done(function (data) {
          // window.open(event.target.href);
        })
        .catch(function (data) {
          // window.open(event.target.href);
        });
});