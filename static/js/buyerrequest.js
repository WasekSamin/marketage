function clickedPost(post_id) {
    document.getElementById(`view__more${post_id}`).style.display = "none";
    document.getElementById(`activepost${post_id}`).style.all = "unset";
}

function clickedSendOffer(post_id) {
    document.getElementById(`seller__viewMore${post_id}`).style.display = "none";
    document.getElementById(`sellerpost${post_id}`).style.all = "unset";
}

function reservedClickedPost(post_id) {
    document.getElementById(`reserved__viewMore${post_id}`).style.display = "none";
    document.getElementById(`reservedpost${post_id}`).style.all = "unset";
}

function activeclickedPost(post_id) {
    document.getElementById(`activeview__more${post_id}`).style.display = "none";
    document.getElementById(`activepost${post_id}`).style.all = "unset";
}

function sellerSendOffer(post_id) {
    document.getElementById(`sellerview__more${post_id}`).style.display = "none";
    document.getElementById(`sellerpost${post_id}`).style.all = "unset";
}