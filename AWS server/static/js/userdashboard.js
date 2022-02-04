let popup = document.getElementById("popup");
        main = document.getElementById("main-sec");
        navbar = document.getElementById("navbar-dash");
        dropdownmenu  = document.getElementById("dropit");
        tablehead = document.getElementsByClassName("table-heading");
        bothmain = document.getElementsByClassName("both");
        sidemenubar = document.getElementById("sidebar");
        var navLinks=document.getElementById("navLinks");
        const slider1=document.getElementById("slider1");
        const slider2=document.getElementById("slider2");
        var d0 = document.getElementById("d0")
        var d1 = document.getElementById("d1")
        var c0 = document.getElementById("c0")
        var c1 = document.getElementById("c1")
        var picedit = document.querySelector('.dropbtn')
        var certedit = document.querySelector('.update')

        picedit.addEventListener("click",openprofEditor);
        certedit.addEventListener("click",opencertEditor)

        function openprofEditor(){
            document.getElementById("editprofile").style.display = "flex";
            main.style.filter = "blur(5px)";
            navbar.style.filter="blur(5px)";
            dropdownmenu.style.display = "none";
        }

        function opencertEditor(){
            document.getElementById("editcertificate").style.display = "flex";
            main.style.filter = "blur(5px)";
            navbar.style.filter="blur(5px)";
            dropdownmenu.style.display = "none";
        }
        

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
        navbar.style.filter="blur(5px)";
        dropdownmenu.style.display = "none";
        }

        function pop_close(){
            popup.style.display = "none";
            main.style.filter = "blur(0px)";
            navbar.style.filter="blur(0px)";
            // dropdownmenu.style.display = "block";
            document.getElementById('editprofile').style.display = "none";
            document.getElementById('editcertificate').style.display = "none";
        }

        function drop_menu(){
            dropdownmenu.style.display = "block";
            tablehead[0].style.position = "unset";
            tablehead[1].style.position = "unset";
            tablehead[2].style.position = "unset";
            tablehead[3].style.position = "unset";
        }

        function pick_menu(){
            dropdownmenu.style.display = "none";
            tablehead[0].style.position="sticky";
            tablehead[1].style.position="sticky";
            tablehead[2].style.position="sticky";
            tablehead[3].style.position="sticky";
        }
        
        function open_menu(){
            // bothmain[0].style.marginLeft = "250px";
            // bothmain[1].style.marginLeft = "250px";
            sidemenubar.style.marginLeft = "0px";
            sidemenubar.style.minWidth="16.5%"
            slider1.style.display = "none";
            slider2.style.display = "flex";
        }
        
        function close_menu(){
            // bothmain[0].style.marginLeft = "0px";
            // bothmain[1].style.marginLeft = "0px";
            sidemenubar.style.marginLeft = "-220px";
            sidemenubar.style.minWidth="0%"
            slider1.style.display = "flex";
            slider2.style.display = "none";
        }

        // document.querySelector('.view').addEventListener('click',pop_open())
