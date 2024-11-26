function sideslide(){
   // Get all elements with the class 'dropdown-btn'
let dropdown = document.getElementsByClassName("nav-link");

for (let i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener("click", function () {
        // Toggle between hiding and showing the dropdown content
        let dropdownContent = this.nextElementSibling;
        if (dropdownContent.style.display === "block") {
            dropdownContent.style.display = "none";
        } else {
            dropdownContent.style.display = "block";
        }
    });
}}