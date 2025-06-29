document.addEventListener("DOMContentLoaded", () => {
  // CATCHY ANIMATION: Dynamic Typing Effect
  const dynamicText = document.getElementById("dynamic-text");
  if (dynamicText) {
    const words = ["Conversation", "Ideas", "Bugs", "Decisions", "Meetings"];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
      const currentWord = words[wordIndex];

      if (isDeleting) {
        // Deleting
        dynamicText.textContent = currentWord.substring(0, charIndex - 1);
        charIndex--;
      } else {
        // Typing
        dynamicText.textContent = currentWord.substring(0, charIndex + 1);
        charIndex++;
      }

      let typeSpeed = isDeleting ? 100 : 200;

      if (!isDeleting && charIndex === currentWord.length) {
        // Pause at end of word
        typeSpeed = 2000;
        isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        wordIndex = (wordIndex + 1) % words.length;
        typeSpeed = 500;
      }

      setTimeout(type, typeSpeed);
    }

    type();
  }

  // CATCHY ANIMATION: Fade In On Scroll
  const fadeInElements = document.querySelectorAll(".fade-in");
  const observerOptions = {
    root: null,
    rootMargin: "0px",
    threshold: 0.1,
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  fadeInElements.forEach((el) => {
    observer.observe(el);
  });

  // Interactive Features Tabs Logic
  const tabButtons = document.querySelectorAll(".tab-button");
  const contentPanes = document.querySelectorAll(".content-pane");
  const indicators = document.querySelectorAll(".indicator");
  const autoPlayBtn = document.getElementById("autoPlayBtn");

  let currentTabIndex = 0;
  let isAutoPlaying = true;
  let autoPlayInterval;

  const tabs = ["colaboracion", "analisis", "automatizacion"];

  // Función para cambiar tab
  function switchTab(targetTab, index) {
    // Deactivate all buttons and panes
    tabButtons.forEach((btn) => btn.classList.remove("active"));
    contentPanes.forEach((pane) => pane.classList.remove("active"));
    indicators.forEach((ind) => ind.classList.remove("active"));

    // Activate the target elements
    const targetButton = document.querySelector(`[data-tab="${targetTab}"]`);
    const targetPane = document.getElementById(targetTab);
    const targetIndicator = indicators[index];

    if (targetButton && targetPane && targetIndicator) {
      targetButton.classList.add("active");
      targetPane.classList.add("active");
      targetIndicator.classList.add("active");

      // Animar métricas
      animateMetrics(targetPane);
    }

    currentTabIndex = index;
  }

  // Auto-play functionality
  function startAutoPlay() {
    autoPlayInterval = setInterval(() => {
      currentTabIndex = (currentTabIndex + 1) % tabs.length;
      switchTab(tabs[currentTabIndex], currentTabIndex);
    }, 4000);
  }

  function stopAutoPlay() {
    clearInterval(autoPlayInterval);
  }

  // Auto-play button control
  if (autoPlayBtn) {
    autoPlayBtn.addEventListener("click", () => {
      isAutoPlaying = !isAutoPlaying;
      const icon = autoPlayBtn.querySelector("i");
      const text = autoPlayBtn.querySelector("span");

      if (isAutoPlaying) {
        startAutoPlay();
        icon.className = "ph-bold ph-pause";
        text.textContent = "Pausar Demo";
      } else {
        stopAutoPlay();
        icon.className = "ph-bold ph-play";
        text.textContent = "Reproducir Demo";
      }
    });
  }

  // Tab button clicks
  tabButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
      const targetTab = button.dataset.tab;
      switchTab(targetTab, tabs.indexOf(targetTab));

      // Pause auto-play when user interacts
      if (isAutoPlaying) {
        stopAutoPlay();
        isAutoPlaying = false;
        if (autoPlayBtn) {
          const icon = autoPlayBtn.querySelector("i");
          const text = autoPlayBtn.querySelector("span");
          icon.className = "ph-bold ph-play";
          text.textContent = "Reproducir Demo";
        }
      }
    });
  });

  // Indicator clicks
  indicators.forEach((indicator, index) => {
    indicator.addEventListener("click", () => {
      switchTab(tabs[index], index);

      // Pause auto-play when user interacts
      if (isAutoPlaying) {
        stopAutoPlay();
        isAutoPlaying = false;
        if (autoPlayBtn) {
          const icon = autoPlayBtn.querySelector("i");
          const text = autoPlayBtn.querySelector("span");
          icon.className = "ph-bold ph-play";
          text.textContent = "Reproducir Demo";
        }
      }
    });
  });

  // Animate metrics function
  function animateMetrics(pane) {
    const metricValues = pane.querySelectorAll(".metric-value");

    metricValues.forEach((value) => {
      const target = Number.parseInt(value.dataset.target);
      let current = 0;
      const increment = target / 50;
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        value.textContent = Math.floor(current);
      }, 30);
    });
  }

  // Start auto-play on load if elements exist
  if (tabButtons.length > 0) {
    startAutoPlay();

    // Initial metrics animation
    setTimeout(() => {
      const activePane = document.querySelector(".content-pane.active");
      if (activePane) {
        animateMetrics(activePane);
      }
    }, 500);
  }

  // Add scroll animations for sections
  const sections = document.querySelectorAll("section");
  const sectionObserverOptions = {
    root: null,
    rootMargin: "0px",
    threshold: 0.1,
  };

  const sectionObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
        observer.unobserve(entry.target);
      }
    });
  }, sectionObserverOptions);

  sections.forEach((section) => {
    section.style.opacity = "0";
    section.style.transform = "translateY(20px)";
    section.style.transition = "opacity 0.6s ease-out, transform 0.6s ease-out";
    sectionObserver.observe(section);
  });

  // Hero particles animation
  const particles = document.querySelectorAll(".particle");
  particles.forEach((particle, index) => {
    particle.style.animationDelay = `${index * 0.5}s`;
  });

  // Smooth scrolling for navigation links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
});
