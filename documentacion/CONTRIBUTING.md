# Guía de Contribución

Bienvenido al repositorio. Sigue estas normas para colaborar efectivamente.

## Normas Básicas del Repositorio
- Trabaja siempre en ramas propias, no en main directamente.
- Mantén el código limpio y comentado.
- No subas archivos grandes o sensibles (usa .gitignore).
-Revisa la documentación antes de hacer cambios importantes

## Estilo de Mensajes de Commit
- Usa mensajes descriptivos en español o inglés.
- Formato: "Tipo: Descripción breve" (e.g., "feat: Añadir función de login", "fix: Corregir error en src/main.py", "docs: Actualizar README").
- Tipos comunes: feat (nueva feature), fix (corrección), docs (documentación), refactor (mejora de código sin cambios funcionales).

## Procedimiento para Modificar README o Documentación
- Crea una rama: `git checkout -b docs/actualizacion-readme`.
- Edita el archivo.
- Guarda tus cambios y haz commit: `git add README.md` y `git commit -m "docs: Actualizar descripción en README"`.
-ENvía tus datos al repositorio remoto con push: `git push origin docs/actualizacion-readme`.
- Crea un Pull Request en GitHub para revisión.

## Flujo de Trabajo Colaborativo
1. Clona el repositorio y actualízalo:
 `git clone <URL_DEL_REPO>`
 `git pull origin main`.
2. Crea una rama: `git checkout -b nombre-rama` (e.g., feature/nueva-funcion).
3. Trabaja y haz commits frecuentes.
4. Push la rama: `git push origin nombre-rama`.
5. En GitHub, crea un Pull Request (PR) de tu rama a main.
6. Asigna revisores (compañeros) para que comenten y aprueben.
7. Fusiona (merge) el PR una vez aprobado.
8. Elimina la rama remota si ya no se necesita.
`git push origin --delete feature/nueva-funcion`
¡Gracias por contribuir!