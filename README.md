## Feishu Approval Fetch Utility

This utility fetches Feishu approval instance details by instance id using an internal app's tenant access token.

### Setup

1. Python 3.9+ recommended.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Set environment variables (recommended via a `.env` file in the project root):

```
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_INSTANCE_ID=A851D76E-6B63-4DD4-91F2-998693422C3C
```

### Run

Use env vars or pass flags:

```bash
python feishu_approval_fetch.py --pretty
# or
python feishu_approval_fetch.py --app-id <APP_ID> --app-secret <APP_SECRET> --instance-id <INSTANCE_ID> --pretty
```

### Notes

- The script calls:
  - `POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal`
  - `POST https://open.feishu.cn/open-apis/approval/v4/instance/get` with `{"instance_id": "..."}`
- Ensure the app has the necessary Approval permissions and is enabled in your tenant.

