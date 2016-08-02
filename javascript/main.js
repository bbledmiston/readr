
function toggle_add_book(event) {
  $(".add_book_form").toggle()
}
function add_book_to_collection(event) {
  console.log("You are adding you're book");
  event.preventDefault();
  // Have to input each text box into a dictionary
  var title = $("#title").val();
  var author = $("#author").val();
  var genre = $("#genre").val();
  var description = $("description").val()
  var book_info = {
    "title": title,
    "author": author,
    "genre": genre,
    "description": description
  }
  $.post(
    "/my_collection",
    JSON.stringify(request_data),
    update_text
  )
}
function update_text(event) {
  console.log("This is that next function");
}

$(document).ready(function() {
$("#add_a_book").click(toggle_add_book)
add_book_to_collection
});
