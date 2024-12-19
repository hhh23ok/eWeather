
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".save-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            const location = this.getAttribute("data-location");
            const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

            fetch("/save-location/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ location }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                    } else {
                        alert(`Error: ${data.message}`);
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    });
});

//Unused function addSaveButtonListeners
// document.addEventListener('DOMContentLoaded', function() {
//     addSaveButtonListeners();
// });
//
// function addSaveButtonListeners() {
//     const saveButtons = document.querySelectorAll(".save-btn");
//     if (saveButtons.length === 0) {
//         console.warn("No save buttons found in the DOM");
//         return;
//     }
//
//     saveButtons.forEach(button => {
//         button.removeEventListener("click", handleSaveClick);
//         button.addEventListener("click", handleSaveClick);
//         console.log("click is added in .js")
//     });
// }
//
// function handleSaveClick(event) {
//     console.log("click is handled")
//     event.preventDefault();
//
//     // if (!isUserAuthenticated()) {
//     //     alert("Please log in to save the location.");
//     //     return;
//     // }
//     //
//     // if (!isBotUserSubscribed()) {
//     //     alert("Please subscribe to the bot to save the location.");
//     //     return;
//     // }
//
//     const location = event.currentTarget.getAttribute("data-location");
//     saveLocation(location);
// }
//
// // function isUserAuthenticated() {
// //     console.log("check auth")
// //     return document.querySelector('.save-btn') !== null; // Change this as per your logic to check user authentication
// // }
//
// // function isBotUserSubscribed() {
// //     console.log("check subscription")
// //     // Check if the user's email matches the bot user's email
// //     const botUserEmail = document.querySelector('.save-btn').getAttribute("data-bot-email");
// //     const userEmail = document.querySelector('.save-btn').getAttribute("data-user-email");
// //
// //     return botUserEmail === userEmail;
// // }
//
// function saveLocation(location) {
//     console.log(`Function saveLocation has been called for location: ${location}`);
//     // Your logic to save the location
// }



(function() {
    "use strict";

    function toggleScrolled() {
        const selectBody = document.querySelector('body');
        const selectHeader = document.querySelector('#header');
        if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
        window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
    }

    document.addEventListener('scroll', toggleScrolled);
    window.addEventListener('load', toggleScrolled);

    const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

    function mobileNavToogle() {
        document.querySelector('body').classList.toggle('mobile-nav-active');
        mobileNavToggleBtn.classList.toggle('bi-list');
        mobileNavToggleBtn.classList.toggle('bi-x');
    }
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);

    document.querySelectorAll('#navmenu a').forEach(navmenu => {
        navmenu.addEventListener('click', () => {
            if (document.querySelector('.mobile-nav-active')) {
              mobileNavToogle();
            }
        });

    });

    document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
        navmenu.addEventListener('click', function(e) {
            e.preventDefault();
            this.parentNode.classList.toggle('active');
            this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
            e.stopImmediatePropagation();
        });
    });

    const preloader = document.querySelector('#preloader');
    if (preloader) {
        window.addEventListener('load', () => {
          preloader.remove();
        });
    }

    // let scrollTop = document.querySelector('.scroll-top');

    // function toggleScrollTop() {
    //     if (scrollTop) {
    //       window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    //     }
    // }
    // scrollTop.addEventListener('click', (e) => {
    //     e.preventDefault();
    //     window.scrollTo({
    //         top: 0,
    //         behavior: 'smooth'
    //     });
    // });
    //
    // window.addEventListener('load', toggleScrollTop);
    // document.addEventListener('scroll', toggleScrollTop);
    //
    // function aosInit() {
    //     AOS.init({
    //         duration: 600,
    //         easing: 'ease-in-out',
    //         once: true,
    //         mirror: false
    //     });
    // }
    // window.addEventListener('load', aosInit);
    //
    // const glightbox = GLightbox({
    //     selector: '.glightbox'
    // });
    //
    // document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
    //     faqItem.addEventListener('click', () => {
    //         faqItem.parentNode.classList.toggle('faq-active');
    //     });
    // });


})();




