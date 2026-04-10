# Josh & Susannah — wedding gallery

Static wedding photo site: HTML gallery + images in the four `Josh and Susannah's Wedding-part-*` folders.  
Live target: [joshandsusannah.com](https://joshandsusannah.com/) (replace the current “coming soon” page once DNS is pointed at Render).

## Local preview

1. Regenerate the gallery (embeds photo list into `index.html`):

   ```bash
   python build_gallery.py
   ```

2. Open `index.html` in a browser, or serve the folder:

   ```bash
   python -m http.server 8080
   ```

   Then visit `http://localhost:8080`.

## GitHub

1. Create a new repository (e.g. `joshandsusannah-wedding`).
2. From this folder:

   ```bash
   git init
   git add .
   git commit -m "Initial wedding site"
   git branch -M main
   git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
   git push -u origin main
   ```

### Large photos

Hundreds of full-size JPEGs can make the repo heavy. Options:

- Keep files under GitHub’s [size limits](https://docs.github.com/repositories/working-with-files/managing-large-files/about-large-files-on-github) (100 MB max per file).
- Use **[Git LFS](https://git-lfs.com/)** for `*.jpg` if needed.

## Render (static site)

1. In [Render](https://dashboard.render.com/), **New → Static Site**.
2. Connect the GitHub repo and select the `main` branch.
3. Settings:
   - **Build command:** `python3 build_gallery.py`
   - **Publish directory:** `.` (repo root)

   If the build ever fails because Python isn’t available, run `python build_gallery.py` locally, commit the updated `index.html`, and set the build command to `echo "skip"` or leave publish directory as `.` with no build step.

4. **Custom domains:** In the service → **Settings → Custom Domains**, add `joshandsusannah.com` and `www.joshandsusannah.com`. Render shows the exact **DNS records** (CNAME / ALIAS / A) to add at your registrar ([custom domains docs](https://render.com/docs/custom-domains)).

5. Optional: this repo includes **`render.yaml`**. You can use Render’s [Blueprint](https://render.com/docs/infrastructure-as-code) flow to create/update the static site from that file (domain entries in YAML may still need verification in the dashboard).

### HTTPS

Render provisions TLS once the custom domain verifies. No extra config is required on your side beyond correct DNS.

## Regenerating after adding photos

Add images under the existing part folders, then:

```bash
python build_gallery.py
git add index.html
git commit -m "Update gallery"
git push
```

Render will rebuild and publish on push (if auto-deploy is on).
