function toggle_add_book(event) {
  $(".add_book_form").toggle();
}

function toggle_prof_info(event) {
  $(".profile_info").toggle();
}

function add_book_to_collection(event) {
  console.log("You are adding you're book");
  var data_sent = {
    "title": $("#title").val(),
    "author": $("#author").val(),
    "genre": $("#genre").val(),
    "description": $("description").val()
  }
  // $.post(
  //   "/my_collection",
  //   data_sent,
  //   received_response
  // );
}

function show_searched(event) {
  event.preventDefault();
  console.log("Searching and than refreshing");
  var info = {
    "text_to_search": $("text_to_search").val()
  }

  $.post(
    "/search_feed",
    info,
    received_response1
  );
}


function received_response(data) {
  console.log(data);
}

function received_response1(data) {
  console.log(data);
}

function update_text(event) {
  console.log("This is that next function");
}

$(document).ready(function() {
  $("#profile_info_button").click(toggle_prof_info)
  $("#add_a_book").click(toggle_add_book)
  $("#submit_new_button").click(add_book_to_collection)
  $("#search_for_book").click(show_searched)
});
