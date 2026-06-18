from fastapi import APIRouter, Depends

from utils.deps import get_current_vendor_user
router = APIRouter()
#  VENDOR DASHBOARD

@router.get("/dashboard")
def vendor_dashboard(
    vendor_user=Depends(get_current_vendor_user)
):
    return {
    
        "vendor_id": vendor_user.id,
        "email": vendor_user.email
    }