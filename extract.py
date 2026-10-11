import fitz,re,csv,json,unicodedata
from pathlib import Path
base=Path(__file__).parent
p=fitz.open('/mnt/data/MPS SMKATB 2026.pdf')
section='PENGURUSAN AM'; title=''; records=[]; tasks={}; names=set(); prev=''
role_pattern=re.compile(r'^(Pengerusi|Timb(?:alan)?\.? Pengerusi|Naib Pengerusi|Setiausaha|S/?U\b|Pen\.? ?(?:Setiausaha|SU|Penyelaras)|AJK\b|Ahli\b|Penyelaras|Bendahari|Juruaudit|Ketua\b|Guru Kanan|Guru Kelas|Guru Penasihat|Pencatat|Warden|Penyelia|Pengurus|Komandan|Penolong|Pemeriksa|Jurulatih|JK Minggu)',re.I)
namepat=re.compile(r'^(?:(?:En|Pn|Cik|Dr|Tn|Dato[’\']?|YM|Ustaz|Ustazah|Hj|Hjh)\.?\s+|(?:Tn\s+Hj|Puan|Encik)\s+)',re.I)
heads=re.compile(r'^\d+(?:\.\d+)?\.\s+(.{5,})$')
def clean(s):return re.sub(r'\s+',' ',s).strip()
for pg in range(41,111):
 text=p[pg].get_text(sort=False)
 if not text.strip():continue
 lines=[clean(x) for x in text.splitlines() if clean(x)]
 region=re.search(r'MPS SMKATB 2026 \(([^)]*)\)',text)
 if region: section=region.group(1).upper()
 currentrole='Ahli / belum disahkan'; lastlabel=''; bullet=[]
 for i,line in enumerate(lines):
  m=heads.match(line)
  if m and len(line)<125 and not any(k in line.lower() for k in ['beriman','tahun 2026']):
   if title and bullet: tasks.setdefault((section,title),[]).extend(bullet)
   title=m.group(1).strip().upper();bullet=[];currentrole='Ahli / belum disahkan';lastlabel='';continue
  if line.startswith(('•','- ')) and len(line)>15:bullet.append(line.lstrip('•- ').strip());continue
  if role_pattern.match(line) and len(line)<75 and not namepat.match(line):currentrole=line;continue
  if namepat.match(line):
   # split trailing role e.g. (K) (Guru Kelas)
   role=currentrole
   if '(K)' in line:role='Ketua / Guru Penasihat'
   elif '(P)' in line:role='Penyelaras / Guru Penasihat'
   if '(Guru Kelas)' in line:role='Guru Kelas'
   name=clean(re.sub(r'\s*\((?:K|P|Guru Kelas)\)\s*$','',line))
   # Avoid some malformed line fragments
   if len(name)<12 or len(name)>100 or 'MPS SMKATB' in name:continue
   label=lastlabel if role in ['Ahli / belum disahkan','Guru Penasihat'] else ''
   records.append(dict(nama=name,bidang=section,jawatankuasa=title or 'TUGAS AM',jawatan=role,konteks=label,muka_surat=pg-2,halaman_pdf=pg+1,status='PERLU SEMAK'))
   names.add(name)
   continue
  if len(line)<65 and not line[0].isdigit() and 'BERIMAN' not in line and not line.startswith('MPS '):
   # labels for table units/classes
   if not re.search(r'^(GK |SU |PK |Ketua |Pembantu |Penolong |Kaunselor|Pengawas|Penyelia)',line,re.I):lastlabel=line
 if title and bullet:tasks.setdefault((section,title),[]).extend(bullet)
# merge exact duplicate
unique={}
for r in records:
 k=(r['nama'],r['bidang'],r['jawatankuasa'],r['jawatan'],r['muka_surat'])
 unique[k]=r
records=list(unique.values())
with open(base/'pelantikan.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['nama','bidang','jawatankuasa','jawatan','konteks','muka_surat','halaman_pdf','status']);w.writeheader();w.writerows(records)
with open(base/'pelantikan.json','w',encoding='utf8') as f:json.dump(records,f,ensure_ascii=False)
with open(base/'bidang_tugas.json','w',encoding='utf8') as f:json.dump([dict(bidang=k[0],jawatankuasa=k[1],tugas=list(dict.fromkeys(v))) for k,v in tasks.items()],f,ensure_ascii=False)
print('Extracted',len(records),'rows',len(names),'distinct exact names',len(tasks),'task blocks')
