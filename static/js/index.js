        let popup = document.getElementById("popup");
        main = document.getElementById("main-sec");

        var navLinks=document.getElementById("navLinks");
        function showMenu(){
            navLinks.style.right="0";
        }
        function hideMenu(){
            navLinks.style.right="-200px";
        }

        function pop_open(){
        // let popup = document.getElementById("popup");
        popup.style.display = "flex";
        main.style.filter = "blur(5px)";
        }

        function pop_close(){
            popup.style.display = "none";
            main.style.filter = "blur(0px)";
        }


        function myFunc() {
            return location;
        }