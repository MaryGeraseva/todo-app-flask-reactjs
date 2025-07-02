# Login Flow Map

## Frontend

- **src/routes/landing/home/page.tsx**
  - **Key:** `<SignInCard />`
  - **Purpose:** Renders the main landing page with tabs for "Sign In" and "Create Account", displaying the login UI.

- **src/routes/landing/home/_components/sign-in/card.tsx**
  - **Key:** `SignInCard`
  - **Purpose:** UI card component that wraps and displays the `SignInForm` for user login.

- **src/routes/landing/home/_components/sign-in/form.tsx**
  - **Key:** `SignInForm`, `onSubmit`
  - **Purpose:** Main login form component. Handles user input, form validation, and submits credentials to the backend `/api/v1/auth/sign-in` endpoint. On success, stores the token and redirects to dashboard.

- **src/schemas/auth-schema.ts**
  - **Key:** `SignInFormSchema`, `TSignInFormSchema`
  - **Purpose:** Zod schema for validating the login form's email and password fields.

- **src/stores/auth-store.ts**
  - **Key:** `useAuthStore`, `signIn(token)`, `isLoggedIn`
  - **Purpose:** Zustand store for authentication state. Stores JWT token and login status; provides `signIn` and `logout` actions.

- **src/routes/landing/root.tsx**
  - **Key:** `LandingRoot`
  - **Purpose:** Root component for the landing section. Redirects to dashboard if already logged in.

---

## Backend

- **flaskr/routes/auth_route.py**
  - **Key:** `SignIn` (class), `/auth/sign-in` (route)
  - **Purpose:** Defines the POST endpoint `/api/v1/auth/sign-in` for user login. Uses `SignInSchema` for request validation and delegates logic to `AuthController.sign_in`.

- **flaskr/controllers/auth_controller.py**
  - **Key:** `AuthController`, `sign_in(data)`
  - **Purpose:** Handles login logic: verifies user credentials, checks password, and returns a JWT token if successful.

- **flaskr/schemas/schema.py**
  - **Key:** `SignInSchema`
  - **Purpose:** Marshmallow schema for validating login request data (inherits from `PlainSignInSchema`).

- **flaskr/schemas/plain_schema.py**
  - **Key:** `PlainSignInSchema`
  - **Purpose:** Defines required fields (`email`, `password`) for login requests.

- **flaskr/models/user_model.py**
  - **Key:** `UserModel`
  - **Purpose:** SQLAlchemy model for user data, including email and hashed password.

- **flaskr/utils.py**
  - **Key:** `check_password(password_hash, password)`
  - **Purpose:** Utility function to verify a plaintext password against a hashed password during login.

- **flaskr/extensions.py**
  - **Key:** `jwt` (JWTManager)
  - **Purpose:** Configures JWT support for authentication token creation and validation.

- **flaskr/__init__.py**
  - **Key:** `create_app`, `api.register_blueprint(auth_route, url_prefix="/api/v1")`
  - **Purpose:** Registers the authentication route and initializes Flask extensions, including JWT.

---

## Flow Summary

1. **User accesses the Sign In tab** (`page.tsx` → `SignInCard` → `SignInForm`).
2. **User submits credentials** via `SignInForm`, validated by `SignInFormSchema`.
3. **Form sends POST request** to `/api/v1/auth/sign-in`.
4. **Backend route** (`auth_route.py`) validates input (`SignInSchema`), calls `AuthController.sign_in`.
5. **Controller** (`auth_controller.py`) checks user in DB (`UserModel`), verifies password (`check_password`), returns JWT token.
6. **Frontend receives token**, stores it in `auth-store.ts` via `signIn`, and redirects user to dashboard.
7. **LandingRoot** ensures logged-in users are redirected away from login page.

---

Only files, classes, and functions directly involved in the login flow are included. This map supports debugging, refactoring, and documentation of the login feature. 