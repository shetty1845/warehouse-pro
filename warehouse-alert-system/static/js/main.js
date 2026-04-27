// ===== DOM Ready =====
document.addEventListener('DOMContentLoaded', () => {
    initAnimations();
    initFlashDismiss();
    initDeleteConfirm();
    initSearchClear();
});

// ===== Staggered card animations =====
function initAnimations() {
    const cards = document.querySelectorAll('.card, .stat-card');
    cards.forEach((card, i) => {
        card.style.animationDelay = `${i * 0.06}s`;
    });
}

// ===== Auto-dismiss flash messages =====
function initFlashDismiss() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-10px)';
            setTimeout(() => flash.remove(), 300);
        }, 4000);

        flash.addEventListener('click', () => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-10px)';
            setTimeout(() => flash.remove(), 300);
        });
    });
}

// ===== Delete confirmation modal =====
function initDeleteConfirm() {
    const deleteLinks = document.querySelectorAll('.btn-delete-trigger');
    const overlay = document.getElementById('deleteModal');
    const confirmBtn = document.getElementById('confirmDelete');
    const cancelBtn = document.getElementById('cancelDelete');

    if (!overlay) return;

    deleteLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const itemName = link.dataset.name;
            const deleteUrl = link.dataset.url;
            document.getElementById('deleteItemName').textContent = itemName;
            confirmBtn.onclick = () => { window.location.href = deleteUrl; };
            overlay.classList.add('show');
        });
    });

    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => overlay.classList.remove('show'));
    }

    if (overlay) {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) overlay.classList.remove('show');
        });
    }
}

// ===== Search clear button =====
function initSearchClear() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput && searchInput.value) {
        searchInput.focus();
    }
}