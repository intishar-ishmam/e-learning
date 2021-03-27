
           function toggleMenu() {
                var x = document.getElementById("nav");
                if (x.className === "navigation") {
                    x.classList.add("toggle-nav");
                } else {
                    x.className = "navigation";
                }
            }
