from emailanalysis.utils import get_text_from_image_url
# url='https://s3.amazonaws.com/s3-ecu/images/ECU_Callout_Trump-TV-CNN_20190619.jpg'
url='https://action.julianforthefuture.com/page/-/2019%20Miami%20Debate%20Promo/allgraphic_20190619_debatepromo.png'
x = get_text_from_image_url(url)
print(x)
