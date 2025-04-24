// TechStore Yönetim Sistemi JavaScript Kodları

// DOM yüklendikten sonra çalışacak kodlar
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap Tooltips etkinleştirme
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Otomatik kapanan alert'ler için zamanlayıcı
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000); // 5 saniye sonra otomatik kapat
    
    // Tarih seçiciler için bugünün tarihini varsayılan olarak ayarla
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        if (!input.value) {
            const today = new Date();
            const year = today.getFullYear();
            let month = today.getMonth() + 1;
            let day = today.getDate();
            
            month = month < 10 ? '0' + month : month;
            day = day < 10 ? '0' + day : day;
            
            input.value = `${year}-${month}-${day}`;
        }
    });
    
    // Tablolar için arama filtresi
    const searchInput = document.getElementById('tableSearchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchText = this.value.toLowerCase();
            const targetTable = document.querySelector(this.dataset.target);
            
            if (targetTable) {
                const rows = targetTable.querySelectorAll('tbody tr');
                rows.forEach(function(row) {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchText) ? '' : 'none';
                });
            }
        });
    }
    
    // Aktif menü öğesini vurgulama
    highlightActiveMenuItem();
});

// Aktif menü öğesini vurgulayan fonksiyon
function highlightActiveMenuItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link, .dropdown-menu .dropdown-item');
    
    navLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            
            // Eğer dropdown içindeyse, üst dropdown'ı da aktif et
            const parentDropdown = link.closest('.dropdown');
            if (parentDropdown) {
                const dropdownToggle = parentDropdown.querySelector('.dropdown-toggle');
                if (dropdownToggle) {
                    dropdownToggle.classList.add('active');
                }
            }
        }
    });
}

// Sayfa yüklenme süresini ölçme
window.addEventListener('load', function() {
    const loadTime = window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart;
    console.log(`Sayfa ${loadTime}ms sürede yüklendi`);
});