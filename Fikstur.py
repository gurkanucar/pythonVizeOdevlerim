import random
import os.path

# dosya yolunu bu şekilde almazsam hata veriyor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

takimlar=[]
path = os.path.join(BASE_DIR, "Takimlar.txt")
file = open(path,"r",encoding= "utf-8")
for i in file:
    # takimları txt den okuyup takimlar isimli listeye ekledik
    takimlar.append(i.replace('\n',""))
file.close()

# basligi yazirdik
path2 = os.path.join(BASE_DIR, "Fikstür.txt")
file = open(path2,"w",encoding= "utf-8")
file.write("\n"+(" "*21)+"KARŞILAŞMALAR")

# takim sayisini dinamik bir şekilde atadık
takimSayisi=len(takimlar)

# müsakabada eşleşen takımların indexlerini tutuyorumki daha sonra ters eşleştirebileyim.
tersiMusabakalar = []

#iki takım arasındaki deplasman ve sahada oynanan maç farklı günlerde olsun diye
#o haftaki maçları kendi arasında 2 li 2 li karıştırıyorum
def HaftadakiMaclariKaristir(x):
    dizi=x[:]
    for i in range(0,(takimSayisi//2)-1):
        rnd = random.randrange(1,(takimSayisi//2)-1,2)
        c=dizi[i]
        d=dizi[i+1]
        dizi[i]= dizi[rnd]
        dizi[i+1]= dizi[rnd-1]
        dizi[rnd]=c
        dizi[rnd-1]=d
    return dizi

# takimSayisi +1 deme sebebim ilk 17 haftayı oluşturacak
# hafta 17 den büyükse de başka bir döngüye girecek ve o döngü içinde
# 18 den 35. haftaya kadar tamamlayacak.
for hafta in range(1, takimSayisi+1):
    # ilk 17 hafta için takımları karşılaştırıyoruz geri kalan 17 haftayı ise
    # tersiMusabakalar isimli diziden çekeceğiz.
    if(hafta <= takimSayisi-1):
        haftalikMusabakalar=[]
        file.write("\n\n"+(" "*22)+str(hafta)+". HAFTA \n")
        sayac = 0
        # her hafta takimSayisi // 2 kadar maç olacak o yüzden bunu koyduk
        while sayac < takimSayisi //2:
            # takımların bir hafta evde bir hafta sahada oynaması için şart koyduk
            if hafta % 2 == 0:
                ilkTakim = random.randint(0, len(takimlar) - 1)
                while(ilkTakim % 2 != 0):
                    ilkTakim = random.randint(0, len(takimlar) - 1)
                ikinciTakim = random.randint(0, len(takimlar) - 1)
                while (ikinciTakim % 2 == 0 and ilkTakim != ikinciTakim):
                    ikinciTakim = random.randint(0, len(takimlar) - 1)
                haftalikMusabakalar.append(ilkTakim)
                haftalikMusabakalar.append(ikinciTakim)
            else:
                ilkTakim = random.randint(0, len(takimlar) - 1)
                while (ilkTakim % 2 == 0):
                    ilkTakim = random.randint(0, len(takimlar) - 1)
                ikinciTakim = random.randint(0, len(takimlar) - 1)
                while (ikinciTakim % 2 != 0 and ilkTakim != ikinciTakim):
                    ikinciTakim = random.randint(0, len(takimlar) - 1)
                haftalikMusabakalar.append(ilkTakim)
                haftalikMusabakalar.append(ikinciTakim)
            # Rastgele çıkan sayıların daha önce çıktıysa burada if şartımıza giriyor
            # ve son eklenen sayılar silinip yerine yenileri üretiliyor
            # ne zaman her sayı 1 kez yazılırsa o zaman eşleşme yaptırıyorum
            # aşağıda if şartına girerse
            # i değeri artamaz ve while döngüsü tekrardan farklı sayılar oluşturur

            if haftalikMusabakalar.count(ilkTakim) > 1 or haftalikMusabakalar.count(ikinciTakim) > 1:
                haftalikMusabakalar.pop(len(haftalikMusabakalar)-1)
                haftalikMusabakalar.pop(len(haftalikMusabakalar)-1)
            else:
                # eğer random çıkan sayılar daha önce çıkmadıysa
                # aralarında müsabaka oluşturuyoruz
                metin = takimlar[ilkTakim] + " - " + takimlar[ikinciTakim]
                # boşluk bıraktım güzel durması için
                metin = " " * (25 - len(takimlar[ilkTakim])) + metin
                file.write(metin + "\n")
                sayac += 1
                # tersiMüsabakalarda hangi index ile hangisi karşılaşmış listeye ekliyorum
                # sonra misal 1 ve 2. index karşılaşmış ise 2 ve 1 numaralı indexi txt ye yazdırıyorum
                tersiMusabakalar.append(ilkTakim)
                tersiMusabakalar.append(ikinciTakim)

    # eğer o an ki hafta sayısı 17 den küçük değil ise
    # tersiMusabakalardan karşılaşmaları çekip yazdırıyoruz.
    else:
        sira = 0
        sayac=0
        for hafta in range(takimSayisi, (takimSayisi * 2) - 1):
            file.write("\n\n" + (" " * 22) + str(hafta) + ". HAFTA \n")
            oHaftakiMaçlar=[]
            while sayac < takimSayisi // 2:
                
                # önce sira+1 diyorum çünkü sira+1. indexteki 17 hafta önce
                # sahada oynayan takım. 
                # sira. indexteki ise 17 hafta önce
                # deplasmanda oynayan takım. ikisini yer değiştirmek için öyle dedim.
                metin = takimlar[tersiMusabakalar[sira + 1]] + " - " + takimlar[tersiMusabakalar[sira]]
                # kenar boşlukları verdik
                metin = " " * (25 - len(takimlar[tersiMusabakalar[sira + 1]])) + metin
                #haftalik maçları karıştırmak için diziyi fonksiyonumuza yolluyoruz
                oHaftakiMaçlar.append(metin)
                sayac += 1
                # 2 arttirma sebebim 0-1 2-3 4-5 şeklinde takımların karşılaşacak olması
                sira += 2
            sayac = 0
            sonDizi = HaftadakiMaclariKaristir(oHaftakiMaçlar)
            #karıştırılmış maçları metin belgesine yazdırıyoruz
            for t in range(0,9):
                file.write(sonDizi[t]+"\n")

print("Fikstür oluşturuldu")