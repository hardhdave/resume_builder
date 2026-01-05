document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("resume-form");
  form.addEventListener("input", updatePreview);

  // Initial dummy data for better UX
  updatePreview();
});

function updatePreview() {
  const data = gatherData();
  renderPreview(data);
}

function gatherData() {
  const getVal = (name) =>
    document.querySelector(`[name="${name}"]`)?.value || "";

  const data = {
    full_name: getVal("full_name"),
    email: getVal("email"),
    phone: getVal("phone"),
    linkedin: getVal("linkedin"),
    github: getVal("github"),
    summary: getVal("summary"),
    skills: getVal("skills"),
    experience: [],
    projects: [],
    education: [],
    certifications: [],
  };

  // Helper to scrape dynamic lists
  const scrapeList = (listId, sectionName) => {
    const list = document.getElementById(listId);
    const items = list.querySelectorAll(".dynamic-item");
    const results = [];
    items.forEach((item) => {
      const obj = {};
      item.querySelectorAll("input, textarea").forEach((input) => {
        if (input.dataset.field) {
          obj[input.dataset.field] = input.value;
        }
      });
      results.push(obj);
    });
    return results;
  };

  data.experience = scrapeList("experience-list", "experience");
  data.projects = scrapeList("projects-list", "projects");
  data.education = scrapeList("education-list", "education");
  data.certifications = scrapeList("certification-list", "certifications");

  // Add template info
  const template = document.getElementById("template-select").value;
  data.template = template;

  // Add font info
  const font = document.getElementById("font-select")?.value || "sans";
  data.font = font;

  return data;
}

// Template Switcher
function changeTemplate(val) {
  const page = document.getElementById("resume-preview");
  // Remove all template classes
  page.classList.remove("template-classic", "template-modern");
  // Add selected
  page.classList.add(`template-${val}`);
}

// Font Switcher
function changeFont(val) {
  const page = document.getElementById("resume-preview");
  // Remove all font classes
  page.classList.remove("font-sans", "font-serif", "font-mono");
  // Add selected
  page.classList.add(`font-${val}`);
}

function renderPreview(data) {
  // Basic Info
  document.getElementById("preview-name").textContent =
    data.full_name || "Your Name";

  const contactParts = [];
  if (data.email) {
    contactParts.push(`<div class="contact-item">${data.email}</div>`);
  }
  if (data.phone) {
    contactParts.push(`<div class="contact-item">${data.phone}</div>`);
  }
  if (data.linkedin) {
    let url = data.linkedin;
    if (!url.startsWith("http")) url = "https://" + url;
    contactParts.push(
      `<div class="contact-item"><a href="${url}" target="_blank">LinkedIn: ${data.linkedin.replace(
        /^https?:\/\//,
        ""
      )}</a></div>`
    );
  }
  if (data.github) {
    let url = data.github;
    if (!url.startsWith("http")) url = "https://" + url;
    contactParts.push(
      `<div class="contact-item"><a href="${url}" target="_blank">GitHub: ${data.github.replace(
        /^https?:\/\//,
        ""
      )}</a></div>`
    );
  }
  document.getElementById("preview-contact").innerHTML = contactParts.join("");

  // Summary
  const summarySection = document.getElementById("preview-summary-section");
  if (data.summary) {
    summarySection.style.display = "block";
    document.getElementById("preview-summary").textContent = data.summary;
  } else {
    summarySection.style.display = "none";
  }

  // Skills
  const skillsSection = document.getElementById("preview-skills-section");
  if (data.skills) {
    skillsSection.style.display = "block";
    document.getElementById("preview-skills").textContent = data.skills;
  } else {
    skillsSection.style.display = "none";
  }

  // Experience
  renderSection(
    "preview-experience-section",
    "preview-experience",
    data.experience,
    (item) => {
      return `
            <div class="resume-item">
                <div class="resume-item-header">
                    <span>${item.title || "Job Title"} ${
        item.company ? "at " + item.company : ""
      }</span>
                    <span>${item.dates || ""}</span>
                </div>
                <div class="resume-text">${(item.description || "").replace(
                  /\n/g,
                  "<br>"
                )}</div>
            </div>
        `;
    }
  );

  // Projects
  renderSection(
    "preview-projects-section",
    "preview-projects",
    data.projects,
    (item) => {
      return `
            <div class="resume-item">
                <div class="resume-item-header">
                    <span>${item.name || "Project Name"} ${
        item.tech ? "(" + item.tech + ")" : ""
      }</span>
                </div>
                <div class="resume-text">${(item.description || "").replace(
                  /\n/g,
                  "<br>"
                )}</div>
            </div>
        `;
    }
  );

  // Education
  renderSection(
    "preview-education-section",
    "preview-education",
    data.education,
    (item) => {
      return `
            <div class="resume-item">
                <div class="resume-item-header">
                    <span>${item.degree || "Degree"}</span>
                    <span>${item.year || ""}</span>
                </div>
                <div class="resume-item-sub">${
                  item.school || "University"
                }</div>
            </div>
        `;
    }
  );

  // Certifications
  renderSection(
    "preview-certification-section",
    "preview-certification",
    data.certifications,
    (item) => {
      return `
            <div class="resume-item">
                 <div class="resume-item-header">
                    <span>${item.name || "Certificate"} ${
        item.issuer ? "- " + item.issuer : ""
      }</span>
                    <span>${item.year || ""}</span>
                </div>
            </div>
        `;
    }
  );
}

function renderSection(sectionId, contentId, items, templateFn) {
  const section = document.getElementById(sectionId);
  const content = document.getElementById(contentId);
  if (items && items.length > 0) {
    section.style.display = "block";
    content.innerHTML = items.map(templateFn).join("");
  } else {
    section.style.display = "none";
  }
}

// Dynamic Form Builders
function addExperience() {
  const id = Date.now();
  const html = `
        <div class="dynamic-item" id="exp-${id}">
            <button type="button" class="btn-remove" onclick="remove('exp-${id}')">&times;</button>
            <div class="form-group">
                <label>Job Title</label>
                <input type="text" class="form-control" data-field="title" placeholder="Software Engineer">
            </div>
            <div class="form-group">
                <label>Company</label>
                <input type="text" class="form-control" data-field="company" placeholder="Acme Corp">
            </div>
            <div class="form-group">
                <label>Dates</label>
                <input type="text" class="form-control" data-field="dates" placeholder="Jan 2020 - Present">
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea class="form-control" data-field="description" placeholder="Achievements..."></textarea>
            </div>
        </div>
    `;
  document
    .getElementById("experience-list")
    .insertAdjacentHTML("beforeend", html);
  updatePreview();
}

function addProject() {
  const id = Date.now();
  const html = `
        <div class="dynamic-item" id="proj-${id}">
            <button type="button" class="btn-remove" onclick="remove('proj-${id}')">&times;</button>
            <div class="form-group">
                <label>Project Name</label>
                <input type="text" class="form-control" data-field="name" placeholder="Portfolio Website">
            </div>
            <div class="form-group">
                <label>Technologies Used</label>
                <input type="text" class="form-control" data-field="tech" placeholder="React, Node.js">
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea class="form-control" data-field="description" placeholder="What did you build?"></textarea>
            </div>
        </div>
    `;
  document
    .getElementById("projects-list")
    .insertAdjacentHTML("beforeend", html);
  updatePreview();
}

function addEducation() {
  const id = Date.now();
  const html = `
        <div class="dynamic-item" id="edu-${id}">
            <button type="button" class="btn-remove" onclick="remove('edu-${id}')">&times;</button>
            <div class="form-group">
                <label>School / University</label>
                <input type="text" class="form-control" data-field="school" placeholder="University of Tech">
            </div>
            <div class="form-group">
                <label>Degree</label>
                <input type="text" class="form-control" data-field="degree" placeholder="B.S. Computer Science">
            </div>
            <div class="form-group">
                <label>Year</label>
                <input type="text" class="form-control" data-field="year" placeholder="2018 - 2022">
            </div>
        </div>
    `;
  document
    .getElementById("education-list")
    .insertAdjacentHTML("beforeend", html);
  updatePreview();
}

function addCertification() {
  const id = Date.now();
  const html = `
        <div class="dynamic-item" id="cert-${id}">
            <button type="button" class="btn-remove" onclick="remove('cert-${id}')">&times;</button>
            <div class="form-group">
                <label>Certificate Name</label>
                <input type="text" class="form-control" data-field="name" placeholder="AWS Certified">
            </div>
            <div class="form-group">
                <label>Issuer</label>
                <input type="text" class="form-control" data-field="issuer" placeholder="Amazon">
            </div>
             <div class="form-group">
                <label>Year</label>
                <input type="text" class="form-control" data-field="year" placeholder="2023">
            </div>
        </div>
    `;
  document
    .getElementById("certification-list")
    .insertAdjacentHTML("beforeend", html);
  updatePreview();
}

function remove(id) {
  document.getElementById(id).remove();
  updatePreview();
}

// Removed background switching functionality

// Download PDF
async function downloadPDF() {
  const data = gatherData();
  const btn = document.querySelector(".btn-primary"); // The download button
  const originalText = btn.textContent;
  btn.textContent = "Generating...";
  btn.disabled = true;

  try {
    const response = await fetch("/api/generate_pdf", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `Resume_${data.full_name || "Draft"}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } else {
      alert("Failed to generate PDF");
    }
  } catch (e) {
    console.error(e);
    alert("Error generating PDF");
  } finally {
    btn.textContent = originalText;
    btn.disabled = false;
  }
}
