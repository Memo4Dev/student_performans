document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(e.target);

    try {
        const data = Object.fromEntries(
            Array.from(formData.entries()).map(([k, v]) => [k, parseFloat(v)])
        );
        
        // show swal message
        Swal.fire({
            title: 'جاري التحليل...',
            text: 'يرجى الانتظار',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('حدث خطأ في الاتصال');
        }

        const result = await response.json();
        const gradeMap = {
            0: 'ممتاز (90-100%)',
            1: 'جيد جدًا (80-89%)',
            2: 'جيد (70-79%)',
            3: 'مقبول (60-69%)',
            4: 'راسب (أقل من 60%)'
        };

        // Determine  background color
        let backgroundColor;
        let textColor = '#000';
        switch(result.prediction) {
            case 0:
                backgroundColor = '#28a745';
                textColor = '#fff';
                break;
            case 1:
                backgroundColor = '#17a2b8';
                textColor = '#fff';
                break;
            case 2:
                backgroundColor = '#ffc107';
                break;
            case 3:
                backgroundColor = '#fd7e14';
                break;
            case 4:
                backgroundColor = '#dc3545';
                textColor = '#fff';
                break;
            default:
                backgroundColor = '#f8f9fa';
        }

        //  show result by SweetAlert
        Swal.fire({
            title: 'نتيجة التحليل',
            html: `
                <div style="font-size: 1.2em; margin: 20px 0;">
                    <strong>الدرجة المتوقعة:</strong><br>
                    <div style="
                        background-color: ${backgroundColor};
                        color: ${textColor};
                        padding: 15px;
                        border-radius: 8px;
                        margin-top: 10px;
                        font-size: 1.3em;
                        font-weight: bold;
                    ">
                        ${gradeMap[result.prediction] || 'غير معروف'}
                    </div>
                </div>
            `,
            icon: 'success',
            confirmButtonText: 'حسناً',
            confirmButtonColor: '#6a11cb'
        });

    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: 'خطأ!',
            text: error.message,
            icon: 'error',
            confirmButtonText: 'حسناً',
            confirmButtonColor: '#dc3545'
        });
    }
});