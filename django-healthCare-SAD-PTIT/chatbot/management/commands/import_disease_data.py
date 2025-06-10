# chatbot/management/commands/import_disease_data.py
from django.core.management.base import BaseCommand
from chatbot.models import Intent, TrainingPhrase, Response

class Command(BaseCommand):
    help = 'Import training data for 10 common diseases in Vietnam'

    def handle(self, *args, **options):
        self.stdout.write('Clearing old data...')
        Intent.objects.all().delete()

        # Disease data
        diseases_data = {
            'cảm_cúm': {
                'description': 'Hỏi về bệnh cảm cúm',
                'phrases': [
                    'bị cảm cúm', 'triệu chứng cảm cúm', 'cảm cúm là gì',
                    'sốt và đau đầu', 'ho và sổ mũi', 'điều trị cảm cúm',
                    'phòng ngừa cảm cúm', 'cảm cúm có nguy hiểm không',
                    'thuốc trị cảm cúm', 'cảm cúm bao lâu thì khỏi'
                ],
                'responses': [
                    (
                        "Cảm cúm là bệnh nhiễm trùng đường hô hấp do virus gây ra.\n\n"
                        "📌 **Triệu chứng thường gặp:**\n"
                        "• Sốt cao (38-40°C)\n"
                        "• Đau đầu, đau mỏi cơ\n"
                        "• Ho khan, đau họng\n"
                        "• Sổ mũi, nghẹt mũi\n"
                        "• Mệt mỏi, chán ăn\n\n"
                        "💊 **Điều trị:**\n"
                        "• Nghỉ ngơi nhiều, uống nhiều nước\n"
                        "• Dùng thuốc hạ sốt (paracetamol)\n"
                        "• Súc miệng nước muối ấm\n"
                        "• Vitamin C tăng sức đề kháng\n\n"
                        "⚠️ **Khi nào cần gặp bác sĩ:**\n"
                        "• Sốt cao trên 39°C kéo dài\n"
                        "• Khó thở, đau ngực\n"
                        "• Ho ra đờm có máu\n"
                        "• Trẻ em dưới 2 tuổi hoặc người già"
                    ),
                    (
                        "🛡️ **Phòng ngừa cảm cúm:**\n"
                        "• Rửa tay thường xuyên bằng xà phòng\n"
                        "• Đeo khẩu trang nơi đông người\n"
                        "• Tránh tiếp xúc người bệnh\n"
                        "• Tiêm vaccine cúm hàng năm\n"
                        "• Tăng cường vitamin C từ trái cây\n"
                        "• Giữ ấm cơ thể khi thời tiết lạnh\n"
                        "• Tập thể dục đều đặn"
                    )
                ]
            },
            'sốt_xuất_huyết': {
                'description': 'Hỏi về bệnh sốt xuất huyết',
                'phrases': [
                    'sốt xuất huyết', 'triệu chứng sốt xuất huyết',
                    'muỗi vằn', 'sốt cao và phát ban', 'chảy máu dưới da',
                    'phòng sốt xuất huyết', 'sốt xuất huyết nguy hiểm',
                    'xét nghiệm sốt xuất huyết', 'điều trị sốt xuất huyết'
                ],
                'responses': [
                    (
                        "Sốt xuất huyết là bệnh truyền nhiễm do virus Dengue gây ra, lây qua muỗi vằn.\n\n"
                        "🔴 **Triệu chứng điển hình:**\n"
                        "• Sốt cao đột ngột (39-40°C)\n"
                        "• Đau đầu dữ dội, đau sau hốc mắt\n"
                        "• Đau cơ, đau khớp\n"
                        "• Phát ban da (ngày 3-4)\n"
                        "• Chảy máu chân răng, nước tiểu\n"
                        "• Tiểu cầu giảm\n\n"
                        "⚠️ **Dấu hiệu nguy hiểm:**\n"
                        "• Đau bụng dữ dội\n"
                        "• Nôn ói liên tục\n"
                        "• Chảy máu bất thường\n"
                        "• Lơ mơ, bứt rứt\n"
                        "• Tay chân lạnh, tím tái\n\n"
                        "💊 **Xử trí:**\n"
                        "• Hạ sốt bằng paracetamol (TUYỆT ĐỐI không dùng aspirin)\n"
                        "• Uống nhiều nước, oresol\n"
                        "• Theo dõi tiểu cầu\n"
                        "• Nhập viện ngay khi có dấu hiệu nguy hiểm"
                    ),
                    (
                        "🛡️ **Phòng ngừa sốt xuất huyết:**\n"
                        "• Diệt muỗi, lăng quăng (bọ gậy)\n"
                        "• Ngủ mùng kể cả ban ngày\n"
                        "• Dọn dẹp các vật chứa nước đọng\n"
                        "• Thả cá vào lu, vại chứa nước\n"
                        "• Phun thuốc diệt muỗi định kỳ\n"
                        "• Mặc quần áo dài tay\n"
                        "• Dùng kem/nhang xua muỗi\n\n"
                        "📅 **Lịch theo dõi bệnh:**\n"
                        "• Ngày 1-3: Sốt cao, theo dõi\n"
                        "• Ngày 3-5: Giai đoạn nguy hiểm\n"
                        "• Ngày 5-7: Hồi phục dần"
                    )
                ]
            },
            'tiêu_chảy': {
                'description': 'Hỏi về bệnh tiêu chảy',
                'phrases': [
                    'bị tiêu chảy', 'đi ngoài nhiều lần', 'đau bụng tiêu chảy',
                    'tiêu chảy cấp', 'mất nước do tiêu chảy', 'điều trị tiêu chảy',
                    'oresol', 'tiêu chảy ở trẻ em', 'nguyên nhân tiêu chảy'
                ],
                'responses': [
                    (
                        "Tiêu chảy là tình trạng đi ngoài phân lỏng trên 3 lần/ngày.\n\n"
                        "🔍 **Nguyên nhân thường gặp:**\n"
                        "• Vi khuẩn, virus (phổ biến nhất)\n"
                        "• Thức ăn bị ôi thiu, nhiễm độc\n"
                        "• Dị ứng thức ăn\n"
                        "• Uống nước không sạch\n"
                        "• Stress, lo lắng\n\n"
                        "💊 **Điều trị:**\n"
                        "• Bù nước và điện giải (Oresol)\n"
                        "• Ăn cháo loãng, bánh mì\n"
                        "• Tránh sữa, đồ cay, dầu mỡ\n"
                        "• Men vi sinh (probiotics)\n"
                        "• Thuốc cầm tiêu chảy (nếu cần)\n\n"
                        "⚠️ **Cần gặp bác sĩ khi:**\n"
                        "• Tiêu chảy có máu/nhầy\n"
                        "• Sốt cao kèm theo\n"
                        "• Mất nước nặng (khát, khô môi)\n"
                        "• Kéo dài trên 3 ngày\n"
                        "• Trẻ dưới 6 tháng tuổi"
                    ),
                    (
                        "🛡️ **Phòng ngừa tiêu chảy:**\n"
                        "• Rửa tay trước khi ăn, sau khi đi vệ sinh\n"
                        "• Ăn chín, uống sôi\n"
                        "• Bảo quản thức ăn đúng cách\n"
                        "• Không ăn đồ ăn để lâu\n"
                        "• Vệ sinh nhà bếp sạch sẽ\n"
                        "• Uống nước đun sôi hoặc đóng chai\n\n"
                        "📝 **Cách pha Oresol:**\n"
                        "• 1 gói Oresol + 200ml nước sôi để nguội\n"
                        "• Uống từng ngụm nhỏ, liên tục\n"
                        "• Trẻ em: 50-100ml sau mỗi lần tiêu\n"
                        "• Người lớn: 200-400ml sau mỗi lần"
                    )
                ]
            },
            'viêm_phổi': {
                'description': 'Hỏi về bệnh viêm phổi',
                'phrases': [
                    'viêm phổi', 'triệu chứng viêm phổi', 'ho có đờm',
                    'khó thở', 'đau ngực khi thở', 'viêm phổi ở trẻ em',
                    'điều trị viêm phổi', 'viêm phổi có lây không'
                ],
                'responses': [
                    (
                        "Viêm phổi là tình trạng nhiễm trùng làm viêm các túi khí trong phổi.\n\n"
                        "🔴 **Triệu chứng:**\n"
                        "• Ho có đờm (vàng, xanh hoặc có máu)\n"
                        "• Sốt cao, ớn lạnh\n"
                        "• Khó thở, thở nhanh nông\n"
                        "• Đau ngực khi thở sâu/ho\n"
                        "• Mệt mỏi, chán ăn\n"
                        "• Ở trẻ em: thở rít, lõm lồng ngực\n\n"
                        "💊 **Điều trị:**\n"
                        "• Kháng sinh (theo chỉ định bác sĩ)\n"
                        "• Thuốc hạ sốt, giảm đau\n"
                        "• Nghỉ ngơi tuyệt đối\n"
                        "• Uống nhiều nước ấm\n"
                        "• Tập thở sâu, ho có kiểm soát\n\n"
                        "⚠️ **Nhập viện ngay nếu:**\n"
                        "• Khó thở nặng, tím tái\n"
                        "• Sốt cao không đáp ứng thuốc\n"
                        "• Lú lẫn, mất phương hướng\n"
                        "• Trẻ dưới 2 tháng tuổi"
                    ),
                    (
                        "🛡️ **Phòng ngừa viêm phổi:**\n"
                        "• Tiêm vaccine phòng viêm phổi\n"
                        "• Không hút thuốc lá\n"
                        "• Rửa tay thường xuyên\n"
                        "• Tránh tiếp xúc người bệnh\n"
                        "• Giữ ấm cơ thể khi trời lạnh\n"
                        "• Tăng cường dinh dưỡng\n\n"
                        "👶 **Với trẻ em:**\n"
                        "• Bú mẹ hoàn toàn 6 tháng đầu\n"
                        "• Tiêm chủng đầy đủ\n"
                        "• Giữ nhà cửa thông thoáng\n"
                        "• Không để trẻ tiếp xúc khói thuốc"
                    )
                ]
            },
            'tay_chân_miệng': {
                'description': 'Hỏi về bệnh tay chân miệng',
                'phrases': [
                    'tay chân miệng', 'nốt phỏng nước ở tay chân',
                    'loét miệng ở trẻ', 'bệnh tay chân miệng',
                    'phòng tay chân miệng', 'tay chân miệng có lây không'
                ],
                'responses': [
                    (
                        "Tay chân miệng là bệnh truyền nhiễm do virus, thường gặp ở trẻ dưới 5 tuổi.\n\n"
                        "🔴 **Triệu chứng điển hình:**\n"
                        "• Sốt nhẹ 1-2 ngày đầu\n"
                        "• Đau họng, chán ăn\n"
                        "• Nốt phỏng nước ở:\n"
                        "  - Lòng bàn tay, bàn chân\n"
                        "  - Mông, háng\n"
                        "  - Trong miệng (loét đau)\n"
                        "• Chảy nước dãi nhiều\n\n"
                        "💊 **Chăm sóc:**\n"
                        "• Hạ sốt bằng paracetamol\n"
                        "• Súc miệng nước muối loãng\n"
                        "• Ăn thức ăn mềm, lỏng, nguội\n"
                        "• Bôi gel làm dịu vết loét miệng\n"
                        "• Giữ vệ sinh sạch sẽ\n\n"
                        "⚠️ **Biến chứng nguy hiểm:**\n"
                        "• Viêm não, viêm màng não\n"
                        "• Viêm cơ tim\n"
                        "• Phù phổi cấp\n"
                        "→ Cần đến viện ngay!"
                    ),
                    (
                        "🛡️ **Phòng ngừa tay chân miệng:**\n"
                        "• Rửa tay xà phòng thường xuyên\n"
                        "• Khử trùng đồ chơi, bề mặt\n"
                        "• Cách ly trẻ bệnh 7-10 ngày\n"
                        "• Không dùng chung đồ ăn uống\n"
                        "• Tránh nơi đông trẻ khi có dịch\n\n"
                        "📝 **Lưu ý quan trọng:**\n"
                        "• Bệnh lây qua đường tiêu hóa\n"
                        "• Virus tồn tại trong phân 1 tháng\n"
                        "• Có thể mắc lại nhiều lần\n"
                        "• Không có vaccine phòng bệnh\n"
                        "• Thường tự khỏi sau 7-10 ngày"
                    )
                ]
            },
            'thủy_đậu': {
                'description': 'Hỏi về bệnh thủy đậu',
                'phrases': [
                    'thủy đậu', 'nổi mụn nước khắp người', 'bệnh thủy đậu',
                    'phòng thủy đậu', 'thủy đậu có để lại sẹo không',
                    'điều trị thủy đậu', 'thủy đậu ở người lớn'
                ],
                'responses': [
                    (
                        "Thủy đậu là bệnh truyền nhiễm do virus Varicella-zoster gây ra.\n\n"
                        "🔴 **Diễn tiến bệnh:**\n"
                        "• Sốt nhẹ, mệt mỏi (1-2 ngày)\n"
                        "• Phát ban đỏ → mụn nước trong\n"
                        "• Mụn nước lan khắp cơ thể\n"
                        "• Ngứa nhiều, mụn vỡ → đóng vảy\n"
                        "• Thời gian: 7-10 ngày\n\n"
                        "💊 **Điều trị:**\n"
                        "• Hạ sốt (paracetamol)\n"
                        "• Thuốc kháng histamin giảm ngứa\n"
                        "• Bôi calamine làm dịu da\n"
                        "• Cắt ngắn móng tay\n"
                        "• Tắm nước ấm, lau nhẹ nhàng\n\n"
                        "⚠️ **Phòng biến chứng:**\n"
                        "• Không gãi để tránh bội nhiễm\n"
                        "• Không bôi thuốc cam, đỏ\n"
                        "• Tránh aspirin (gây hội chứng Reye)"
                    ),
                    (
                        "🛡️ **Phòng ngừa thủy đậu:**\n"
                        "• Tiêm vaccine thủy đậu\n"
                        "• Cách ly người bệnh\n"
                        "• Tránh tiếp xúc với:\n"
                        "  - Phụ nữ mang thai\n"
                        "  - Trẻ sơ sinh\n"
                        "  - Người suy giảm miễn dịch\n\n"
                        "📝 **Lưu ý quan trọng:**\n"
                        "• Lây qua đường hô hấp\n"
                        "• Lây mạnh 1-2 ngày trước phát ban\n"
                        "• Miễn dịch suốt đời sau khi mắc\n"
                        "• Virus tồn tại → zona sau này\n"
                        "• Người lớn thường bệnh nặng hơn trẻ"
                    )
                ]
            },
            'sởi': {
                'description': 'Hỏi về bệnh sởi',
                'phrases': [
                    'bệnh sởi', 'triệu chứng sởi', 'phát ban sởi',
                    'phòng bệnh sởi', 'vaccine sởi', 'sởi ở trẻ em',
                    'biến chứng sởi', 'điều trị sởi'
                ],
                'responses': [
                    (
                        "Sởi là bệnh truyền nhiễm cấp tính do virus sởi gây ra.\n\n"
                        "🔴 **Triệu chứng theo giai đoạn:**\n"
                        "• Giai đoạn ủ bệnh: 10-14 ngày\n"
                        "• Khởi phát: Sốt cao, ho, sổ mũi\n"
                        "• Hạt Koplik trong miệng (chấm trắng)\n"
                        "• Phát ban từ mặt → toàn thân\n"
                        "• Ban mờ dần theo thứ tự xuất hiện\n\n"
                        "💊 **Điều trị hỗ trợ:**\n"
                        "• Hạ sốt, nghỉ ngơi\n"
                        "• Vitamin A liều cao\n"
                        "• Uống nhiều nước\n"
                        "• Chăm sóc mắt, miệng\n"
                        "• Kháng sinh nếu bội nhiễm\n\n"
                        "⚠️ **Biến chứng nguy hiểm:**\n"
                        "• Viêm phổi (phổ biến nhất)\n"
                        "• Viêm não\n"
                        "• Tiêu chảy nặng\n"
                        "• Viêm tai giữa"
                    ),
                    (
                        "🛡️ **Phòng ngừa sởi:**\n"
                        "• Tiêm vaccine MMR:\n"
                        "  - Mũi 1: 12-15 tháng\n"
                        "  - Mũi 2: 4-6 tuổi\n"
                        "• Cách ly người bệnh\n"
                        "• Đeo khẩu trang\n"
                        "• Tăng cường dinh dưỡng\n\n"
                        "📝 **Thông tin quan trọng:**\n"
                        "• Lây qua đường hô hấp\n"
                        "• Lây mạnh 4 ngày trước và sau phát ban\n"
                        "• Miễn dịch suốt đời sau mắc bệnh\n"
                        "• Nguy hiểm với trẻ dưới 5 tuổi\n"
                        "• Có thể phòng được bằng vaccine"
                    )
                ]
            },
            'viêm_gan_B': {
                'description': 'Hỏi về bệnh viêm gan B',
                'phrases': [
                    'viêm gan B', 'viêm gan siêu vi B', 'xét nghiệm HBsAg',
                    'lây truyền viêm gan B', 'điều trị viêm gan B',
                    'phòng viêm gan B', 'viêm gan B mãn tính'
                ],
                'responses': [
                    (
                        "Viêm gan B là bệnh nhiễm virus HBV gây tổn thương gan.\n\n"
                        "🔴 **Triệu chứng:**\n"
                        "• Giai đoạn cấp:\n"
                        "  - Mệt mỏi, chán ăn\n"
                        "  - Vàng da, vàng mắt\n"
                        "  - Nước tiểu sẫm màu\n"
                        "  - Đau tức vùng gan\n"
                        "• Nhiều người không có triệu chứng\n\n"
                        "💊 **Điều trị:**\n"
                        "• Viêm gan B cấp: điều trị triệu chứng\n"
                        "• Viêm gan B mãn: thuốc kháng virus\n"
                        "• Theo dõi định kỳ 6 tháng\n"
                        "• Tránh rượu bia tuyệt đối\n"
                        "• Chế độ ăn lành mạnh\n\n"
                        "⚠️ **Biến chứng:**\n"
                        "• Xơ gan\n"
                        "• Ung thư gan\n"
                        "• Suy gan cấp"
                    ),
                    (
                        "🛡️ **Phòng ngừa viêm gan B:**\n"
                        "• Tiêm vaccine viêm gan B:\n"
                        "  - Sơ sinh: trong 24h đầu\n"
                        "  - 3 mũi: 0-1-6 tháng\n"
                        "• Không dùng chung kim tiêm\n"
                        "• Quan hệ tình dục an toàn\n"
                        "• Xét nghiệm trước mang thai\n\n"
                        "📝 **Đường lây truyền:**\n"
                        "• Qua máu và dịch cơ thể\n"
                        "• Từ mẹ sang con\n"
                        "• Quan hệ tình dục không an toàn\n"
                        "• KHÔNG lây qua:\n"
                        "  - Ăn uống chung\n"
                        "  - Hôn, ôm thông thường\n"
                        "  - Ho, hắt hơi"
                    )
                ]
            },
            'lao_phổi': {
                'description': 'Hỏi về bệnh lao phổi',
                'phrases': [
                    'bệnh lao phổi', 'ho ra máu', 'ho kéo dài',
                    'điều trị lao', 'lao phổi có lây không',
                    'xét nghiệm lao', 'phòng bệnh lao'
                ],
                'responses': [
                    (
                        "Lao phổi là bệnh truyền nhiễm do vi khuẩn Mycobacterium tuberculosis.\n\n"
                        "🔴 **Triệu chứng điển hình:**\n"
                        "• Ho kéo dài > 2 tuần\n"
                        "• Ho ra đờm, có thể ra máu\n"
                        "• Sốt nhẹ về chiều\n"
                        "• Ra mồ hôi đêm\n"
                        "• Sút cân không rõ nguyên nhân\n"
                        "• Mệt mỏi, chán ăn\n\n"
                        "💊 **Điều trị:**\n"
                        "• Phác đồ 6 tháng (2RHZE/4RH)\n"
                        "• Uống thuốc đều đặn, đủ liều\n"
                        "• Không được bỏ thuốc giữa chừng\n"
                        "• Kiểm tra định kỳ\n"
                        "• Cách ly 2 tuần đầu điều trị\n\n"
                        "⚠️ **Quan trọng:**\n"
                        "• Điều trị đủ liều để tránh kháng thuốc\n"
                        "• Theo dõi tác dụng phụ của thuốc"
                    ),
                    (
                        "🛡️ **Phòng ngừa lao phổi:**\n"
                        "• Tiêm BCG cho trẻ sơ sinh\n"
                        "• Che miệng khi ho, hắt hơi\n"
                        "• Thông thoáng nhà cửa\n"
                        "• Khám sức khỏe định kỳ\n"
                        "• Điều trị dự phòng nếu tiếp xúc\n\n"
                        "📝 **Lưu ý:**\n"
                        "• Lây qua đường hô hấp\n"
                        "• Không phải ai nhiễm cũng phát bệnh\n"
                        "• Có thể chữa khỏi hoàn toàn\n"
                        "• Miễn phí điều trị tại Việt Nam\n"
                        "• Cần kiên trì điều trị đủ 6 tháng"
                    )
                ]
            },
            'tiểu_đường': {
                'description': 'Hỏi về bệnh tiểu đường',
                'phrases': [
                    'bệnh tiểu đường', 'đường huyết cao', 'triệu chứng tiểu đường',
                    'type 1 type 2', 'kiểm soát tiểu đường', 'biến chứng tiểu đường',
                    'chế độ ăn tiểu đường', 'thuốc tiểu đường'
                ],
                'responses': [
                    (
                        "Tiểu đường là bệnh rối loạn chuyển hóa đường trong máu.\n\n"
                        "🔴 **Triệu chứng 3 nhiều 1 ít:**\n"
                        "• Tiểu nhiều (nhất là ban đêm)\n"
                        "• Khát nhiều\n"
                        "• Ăn nhiều\n"
                        "• Sút cân (ít cân)\n"
                        "• Mệt mỏi, ngứa da\n"
                        "• Vết thương lâu lành\n\n"
                        "💊 **Kiểm soát:**\n"
                        "• Thuốc hạ đường huyết/insulin\n"
                        "• Chế độ ăn kiêng đường, tinh bột\n"
                        "• Tập thể dục đều đặn\n"
                        "• Kiểm tra đường huyết thường xuyên\n"
                        "• Khám định kỳ 3 tháng\n\n"
                        "⚠️ **Biến chứng:**\n"
                        "• Tim mạch, đột quỵ\n"
                        "• Suy thận\n"
                        "• Mù mắt\n"
                        "• Cắt cụt chi"
                    ),
                    (
                        "🛡️ **Phòng ngừa tiểu đường type 2:**\n"
                        "• Duy trì cân nặng hợp lý\n"
                        "• Ăn uống lành mạnh:\n"
                        "  - Hạn chế đường, tinh bột\n"
                        "  - Nhiều rau xanh, ngũ cốc\n"
                        "  - Chia nhỏ bữa ăn\n"
                        "• Tập thể dục 30 phút/ngày\n"
                        "• Không hút thuốc lá\n"
                        "• Khám sàng lọc định kỳ\n\n"
                        "📝 **Chỉ số cần nhớ:**\n"
                        "• Đường huyết lúc đói: < 7 mmol/L\n"
                        "• HbA1c: < 7%\n"
                        "• Huyết áp: < 130/80 mmHg\n"
                        "• Mỡ máu: LDL < 2.6 mmol/L"
                    )
                ]
            }
        }

        # Basic intents
        basic_intents = {
            'chào_hỏi': {
                'description': 'Người dùng chào hỏi',
                'phrases': [
                    'xin chào', 'chào bạn', 'hello', 'hi',
                    'chào buổi sáng', 'chào buổi chiều'
                ],
                'responses': [
                    (
                        "Xin chào! Tôi là trợ lý y tế AI. Tôi có thể tư vấn về 10 bệnh phổ biến tại Việt Nam. "
                        "Bạn cần biết thông tin về bệnh nào?"
                    ),
                    (
                        "Chào bạn! Tôi có thể giúp bạn tìm hiểu về các bệnh như: cảm cúm, sốt xuất huyết, tiêu chảy, "
                        "viêm phổi, tay chân miệng, thủy đậu, sởi, viêm gan B, lao phổi và tiểu đường. "
                        "Bạn quan tâm đến bệnh nào?"
                    )
                ]
            },
            'danh_sách_bệnh': {
                'description': 'Hỏi về các bệnh có thể tư vấn',
                'phrases': [
                    'có những bệnh nào', 'tư vấn bệnh gì', 'danh sách bệnh',
                    'bệnh phổ biến', 'các bệnh thường gặp'
                ],
                'responses': [
                    (
                        "Tôi có thể tư vấn về 10 bệnh phổ biến tại Việt Nam:\n\n"
                        "1. **Cảm cúm** - Bệnh nhiễm virus đường hô hấp\n"
                        "2. **Sốt xuất huyết** - Do muỗi vằn truyền bệnh\n"
                        "3. **Tiêu chảy** - Rối loạn tiêu hóa thường gặp\n"
                        "4. **Viêm phổi** - Nhiễm trùng phổi\n"
                        "5. **Tay chân miệng** - Bệnh truyền nhiễm ở trẻ em\n"
                        "6. **Thủy đậu** - Bệnh nổi mụn nước toàn thân\n"
                        "7. **Sởi** - Bệnh phát ban do virus\n"
                        "8. **Viêm gan B** - Nhiễm virus viêm gan\n"
                        "9. **Lao phổi** - Bệnh lao ở phổi\n"
                        "10. **Tiểu đường** - Rối loạn chuyển hóa đường\n\n"
                        "Bạn muốn tìm hiểu về bệnh nào?"
                    )
                ]
            },
            'cảm_ơn': {
                'description': 'Người dùng cảm ơn',
                'phrases': [
                    'cảm ơn', 'cám ơn', 'thanks', 'thank you',
                    'cảm ơn bạn', 'cảm ơn nhiều'
                ],
                'responses': [
                    (
                        "Không có chi! Rất vui được giúp đỡ bạn. Nếu cần thêm thông tin về sức khỏe, đừng ngần ngại hỏi nhé!"
                    ),
                    (
                        "Rất vui được hỗ trợ bạn! Chúc bạn luôn mạnh khỏe. Hãy nhớ phòng bệnh hơn chữa bệnh nhé!"
                    )
                ]
            }
        }

        # Merge all intents
        all_intents = {**diseases_data, **basic_intents}

        # Import to database
        for intent_name, data in all_intents.items():
            intent = Intent.objects.create(
                name=intent_name,
                description=data['description']
            )
            for phrase in data['phrases']:
                TrainingPhrase.objects.create(
                    intent=intent,
                    text=phrase
                )
            for idx, response_text in enumerate(data['responses']):
                Response.objects.create(
                    intent=intent,
                    text=response_text,
                    priority=len(data['responses']) - idx
                )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {len(all_intents)} intents with training data'
        ))

        # Train chatbot
        from chatbot.bot import ChatBot
        bot = ChatBot()
        bot.train_from_database()
        self.stdout.write(self.style.SUCCESS('Chatbot trained successfully!'))
