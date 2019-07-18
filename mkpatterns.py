import os, sys
from unicodedata import normalize

VOWELS = [
   "a", "ā", "i", "ī", "u", "ū",
   "ṛ", "ṝ", "ḷ", "ḹ",
   "e", "ai", "o", "au",
]

# Vedic variants
for p in VOWELS.copy():
   VOWELS.append(normalize("NFC", p + "\N{COMBINING ACUTE ACCENT}"))
   VOWELS.append(normalize("NFC", p + "\N{COMBINING GRAVE ACCENT}"))

# Other ways to write liquids
for p in VOWELS.copy():
   p = normalize("NFD", p)
   p2 = p.replace("\N{COMBINING DOT BELOW}", "\N{COMBINING RING BELOW}")
   if p2 != p:
      VOWELS.append(normalize("NFC", p2))

SPECIALS = ["ṃ", "ṁ", "m̐", "ḥ", "ẖ", "ḫ"]

CONSONANTS = [
   "k", "kh", "g", "gh", "ṅ",
   "c", "ch", "j", "jh", "ñ",
   "ṭ", "ṭh", "ḍ", "ḍh", "ṇ",
   "t", "th", "d", "dh", "n",
   "p", "ph", "b", "bh", "m",
   "y", "r", "l", "v",
   "ś", "ṣ", "s", "h",
]

def extract_leading_consonants(s):
   i = 0
   while i < len(s) and not s[i:].startswith(tuple(VOWELS)) and not s[i:].startswith("-"):
      i += 1
   return s[:i]

NOT_CLUSTERS = {"tt", "str", "lp", "śc", "ṣṭ"}  # Exceptions

def load_clusters():
   clusters = set()
   with open("monier.txt") as fp:
      for word in fp:
         word = normalize("NFC", word.strip())
         cluster = extract_leading_consonants(word)
         if len(cluster) > 1 and cluster not in NOT_CLUSTERS:
            clusters.add(cluster)
   return clusters

CLUSTERS = load_clusters()
CLUSTERS |= {"kṣy"}

rules = set()

def unseparable(s):
   return "".join(c + "2" for c in s)

# We only break _before_ a syllable, so we don't really care about what
# exactly ends the syllable. We only need it to be a kind of vowel.
def trim_vowels(vowels):
   tmp = set(vowels)
   for v in vowels:
      tmp.add(normalize("NFD", v))
   tmp = sorted(tmp, key=lambda v: len(v))
   rv = set()
   while tmp:
      r = tmp.pop()
      if not any(r.startswith(v) for v in tmp):
         rv.add(r)
   return sorted(rv)

starters = sorted(set(CLUSTERS) | set(CONSONANTS))
for s in starters:
   for v in trim_vowels(VOWELS):
      rules.add("1%s%s" % (unseparable(s), v))
      rules.add("1%s%s" % (unseparable(normalize("NFD", s)), v))

for p in SPECIALS:
   rules.add("2%s1" % p)
   rules.add("2%s1" % normalize("NFD", p))

rules = sorted(rules)
rules = "\n".join(rules)

with open("patterns.tpl") as fp:
   code = fp.read()

code = code.replace("$PATTERNS", rules)
sys.stdout.write(code)
