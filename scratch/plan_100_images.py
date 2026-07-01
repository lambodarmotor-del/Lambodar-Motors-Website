import json
import os
import re

workspace_dir = r"c:\Users\Harshil\OneDrive\Desktop\website"
blog_dir = os.path.join(workspace_dir, "blog")

html_files = [f for f in os.listdir(blog_dir) if f.endswith(".html") and f not in ["index.html", "blog-template.html"]]
html_files.sort()

# Create a list of titles
# Let's map titles based on the file contents
file_to_title = {}
for bf in html_files:
    path = os.path.join(blog_dir, bf)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    title_match = re.search(r'<h1 class="post-title">(.*?) \| Gota, Ahmedabad</h1>', content)
    if not title_match:
        title_match = re.search(r'<h1 class="post-title">(.*?)</h1>', content)
    if title_match:
        file_to_title[bf] = title_match.group(1).split(" | ")[0].strip()
    else:
        file_to_title[bf] = bf.replace(".html", "").replace("-", " ").title()

# We will generate a unique prompt for each of the 100 topics
prompts_plan = []
for idx, bf in enumerate(html_files):
    title = file_to_title[bf]
    t = title.lower()
    
    # Extract clean list of words to prevent substring issues (like 'ac' matching 'mechanic')
    words = set(re.findall(r'[a-z0-9]+', t))
    
    # Default prompt fallback
    prompt = f"A professional car workshop photo related to {title}, realistic photography, high definition, detailed garage setting"
    
    # Specialized prompts to ensure maximum variety
    if 'ac' in words or 'cooling' in words or 'air conditioning' in t:
        if 'cost' in words or 'price' in words or 'pricing' in words:
            prompt = "A close-up of a digital pressure gauge showing pressure readings on a car AC system recharge kit, realistic garage setting, high definition"
        elif 'smell' in words or 'bad smell' in t:
            prompt = "A mechanic cleaning a car dashboard ventilation grid with an AC sanitizing spray foam, cabin interior detail, realistic photography"
        elif 'compressor' in words:
            prompt = "A brand new shiny car AC compressor unit sitting on a wooden workbench next to mechanic tools, realistic photography"
        elif 'signs' in words or 'warning' in words:
            prompt = "A close-up of an automotive AC vent with ice frost forming on the metal grill, car interior view, realistic photography"
        else:
            prompt = "A technician checking AC pipes under the hood of a car with a leak detection flashlight, realistic photography"
            
    elif 'engine' in words or 'diagnose' in words or 'diagnosis' in words or 'obd' in words or 'light' in words or 'spark' in words:
        if 'light' in words:
            prompt = "A close-up of a car dashboard instrument cluster with a bright yellow Check Engine warning light illuminated, realistic photography"
        elif 'oil' in words:
            if 'viscosity' in words or 'grade' in words:
                prompt = "A mechanic pouring golden, high-grade engine oil from a branded container into a car engine oil cap, realistic photography"
            else:
                prompt = "A clean oil dipstick showing fresh golden oil level held by a mechanic wearing black gloves, realistic garage photography"
        elif 'scanner' in words or 'scan' in words:
            prompt = "An advanced automotive OBD-II diagnostic scanner screen displaying live data graphs inside a car cabin, realistic photography"
        elif 'overhaul' in words or 'rebuild' in words or 'repair' in words:
            prompt = "An open cylinder head of a car engine undergoing rebuild, pistons and valves visible, clean engine bay workshop setting, realistic photography"
        else:
            prompt = "A technician inspecting wiring harnesses and spark plugs inside a modern clean car engine bay, realistic photography"
            
    elif 'denting' in words or 'painting' in words or 'paint' in words or 'bumper' in words or 'scratch' in words or 'rust' in words or 'panel' in words or 'dent' in words:
        if 'bumper' in words:
            prompt = "A mechanic in a workshop aligning and attaching a brand new black rear bumper to a silver sedan, realistic photography"
        elif 'scratch' in words:
            prompt = "A close-up of a car paint surface showing a clear reflection of workshop lights with minor paint scratches being inspected, realistic photography"
        elif 'rust' in words:
            prompt = "A technician using a pneumatic sander to grind away rust bubbles from a car wheel arch panel, sparks flying, realistic photography"
        elif 'paint booth' in t or 'spray' in words:
            prompt = "A spray painter in a full protective suit and mask spraying metallic silver paint on a car door inside a heated downdraft booth, realistic photography"
        elif 'difference' in words or 'vs' in words:
            prompt = "A split screen panel in a workshop showing a dented door on the left and a perfectly primed gray door panel on the right, realistic photography"
        elif 'correctly' in words or 'inspected' in words:
            prompt = "A quality inspector checking paint finish gloss on a car door using a handheld gloss meter under bright inspection lights, realistic photography"
        else:
            prompt = "A panel beater using a stud welder dent puller tool to pull out a dent on a dark grey car door panel, realistic photography"
            
    elif 'detailing' in words or 'spa' in words or 'wash' in words or 'polish' in words or 'ceramic' in words:
        if 'ceramic' in words:
            prompt = "Water droplets perfectly beading on a highly reflective black car hood treated with premium ceramic coating, realistic photography"
        elif 'wash' in words:
            prompt = "A car covered in thick white snow foam wash soap inside a professional detailing bay, realistic photography"
        elif 'polish' in words or 'buff' in words:
            prompt = "A detailer using a dual-action rotary buffer machine with a yellow foam pad on a black car fender, realistic photography"
        elif 'interior' in words or 'vacuum' in words:
            prompt = "A detailer deep vacuuming a car dashboard and steering wheel with a thin crevice tool attachment, realistic photography"
        else:
            prompt = "A row of premium detailing chemical bottles and microfiber towels neatly arranged on a metal shelf in a garage, realistic photography"
            
    elif 'alignment' in words or 'tire' in words or 'tires' in words or 'rotation' in words or 'chassis' in words or 'suspension' in words or 'brakes' in words or 'brake' in words or 'pad' in words:
        if 'alignment' in words:
            prompt = "A laser wheel alignment setup showing green laser lines projected onto a car tire tread in a garage, realistic photography"
        elif 'rotation' in words:
            prompt = "A mechanic using a pneumatic impact wrench to loosen lug nuts on a car tire raised on a hydraulic lift, realistic photography"
        elif 'wear' in words or 'new tires' in t or 'tires' in words:
            prompt = "A close-up of a digital tread depth gauge measuring the tread depth on a car tire, realistic photography"
        elif 'brakes' in words or 'brake' in words or 'pad' in words or 'pads' in words:
            prompt = "A mechanic installing a brand new red brake caliper and metallic brake disc on a car hub, realistic photography"
        else:
            prompt = "A technician inspecting the rear coil spring suspension and shock absorber assembly of a car on a lift, realistic photography"
            
    elif 'trust' in words or 'trusting' in words or 'honest' in words or 'red flag' in t or 'scam' in words or 'find' in words or 'choose' in words or 'ask' in words or 'reputation' in words:
        if 'scam' in words or 'honest' in words or 'red flag' in t:
            prompt = "A mechanic showing a worn-out spark plug directly to a car owner inside a clean workshop, talking in a friendly manner, realistic photography"
        elif 'questions' in words or 'ask' in words or 'calling' in words:
            prompt = "A close-up of a clipboard with an auto repair checklist and a pen sitting on a clean counter in a workshop reception, realistic photography"
        else:
            prompt = "A friendly service adviser in a clean uniform handing over car keys to a smiling customer in a workshop bay, realistic photography"
            
    elif 'used car' in t or 'purchase' in words or 'buying' in words or 'inspection' in words or 'inspect' in words or 'inspected' in words:
        if 'pre purchase' in t or 'used car' in t:
            prompt = "A mechanic inspecting under the chassis of a raised car with a work light, writing on an inspection checklist, realistic photography"
        elif 'pre-purchase' in t or 'inspect a used car' in t:
            prompt = "A mechanic inspecting under the chassis of a raised car with a work light, writing on an inspection checklist, realistic photography"
        else:
            prompt = "A diagnostic tablet showing vehicle inspection results resting on the passenger seat of a car, realistic photography"
            
    elif 'insurance' in words or 'claim' in words or 'deductible' in words or 'totaled' in words or 'total loss' in t or 'accident' in words:
        if 'deductible' in words or 'claim' in words:
            prompt = "A close-up of insurance claim paperwork, a calculator, and car keys on a wooden office desk in a workshop, realistic photography"
        elif 'accident' in words or 'crash' in words:
            prompt = "A clipboard with a collision repair damage assessment form resting on a crumpled car front fender, realistic photography"
        else:
            prompt = "An insurance surveyor taking a photo of a dented car side panel using a smartphone in a workshop bay, realistic photography"
            
    elif 'cost' in words or 'price' in words or 'pricing' in words or 'budget' in words or 'afford' in words or 'finance' in words or 'save money' in t:
        if 'finance' in words:
            prompt = "A hand holding a pen signing a flexible monthly payment plan document next to a car key on a desk, realistic photography"
        else:
            prompt = "A close-up of a printed, itemized auto repair quote invoice next to a key fob on a desk, clean modern typography, realistic photography"
            
    elif 'transmission' in words or 'manual' in words or 'automatic' in words:
        prompt = "A transmission gearbox assembly casing opened on a clean metal workbench, gears and shafts visible, realistic photography"
        
    elif 'lifespan' in words or 'extend' in words or 'regular' in words or 'upkeep' in words or 'benefit' in words or 'maintenance' in words:
        prompt = "A clean car engine bay with all caps highlighted (coolant, oil, washer fluid), detailed overview, realistic photography"

    # Category and theme
    if any(w in words for w in ["near me", "gota", "ahmedabad", "find", "choose", "honest", "scam", "trust", "best", "review", "reviews"]):
        category = "local"
    else:
        category = "service"

    prompts_plan.append({
        "index": idx,
        "filename": bf,
        "title": title,
        "category": category,
        "image_filename": f"blog_post_unique_{idx}.png", # matching existing filename in HTML files
        "prompt": prompt
    })

# Save plan to scratch directory
plan_path = os.path.join(workspace_dir, "scratch", "image_generation_plan.json")
os.makedirs(os.path.dirname(plan_path), exist_ok=True)
with open(plan_path, "w", encoding="utf-8") as f:
    json.dump(prompts_plan, f, indent=2)

print(f"Saved image generation plan with {len(prompts_plan)} unique prompts to scratch/image_generation_plan.json")
