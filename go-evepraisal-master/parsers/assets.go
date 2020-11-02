package main
import "C"
import (
	"fmt"
	"regexp"
	"sort"
	"strings"
	"strconv"
)


type Input map[int]string
//export Add
type ParserResult interface {
	// Name is the name of the PARSER that yielded this result
	Name() string
	Lines() []int
}
//export Add
var bigNumberRegex = `[\d,'\.\ ’` + "\u00a0\xc2\xa0’" + `]`
var cleanIntegers = regexp.MustCompile(`[,\'\.\ ’` + "\u00a0\xc2\xa0" + `]`)
var separatorCharacters = map[rune]bool{
	',':    true,
	'.':    true,
	' ':    true,
	'\'':   true,
	'\xc2': true,
	'\xa0': true,
	'’':    true,
}
//export splitDecimal
func splitDecimal(s string) (string, string) {
	runes := []rune(s)
	if len(runes) > 3 {
		_, twodecimal := separatorCharacters[runes[len(runes)-3]]
		if twodecimal {
			whole := string(runes[0 : len(runes)-3])
			decimal := string(runes[len(runes)-2:])
			return whole, decimal
		}
	}
	if len(runes) > 2 {
		_, onedecimal := separatorCharacters[runes[len(runes)-2]]
		if onedecimal {
			whole := string(runes[0 : len(runes)-2])
			decimal := string(runes[len(runes)-1:])
			return whole, decimal
		}
	}

	return s, ""
}

// ToInt parses a string into an integer. It will return 0 on failure
func ToInt(s string) int64 {
	if s == "" {
		return 0
	}

	whole, _ := splitDecimal(s)
	cleaned := cleanIntegers.ReplaceAllString(whole, "")

	i, err := strconv.ParseInt(cleaned, 10, 64)
	if err == nil {
		return i
	}

	return 0
}

// ToFloat64 parses a string into a float64. It will return 0.0 on failure
func ToFloat64(s string) float64 {
	// Attempt to parse float as "normal"
	f, err := strconv.ParseFloat(s, 64)
	if err == nil {
		return f
	}

	whole, decimal := splitDecimal(s)
	f, _ = strconv.ParseFloat(fmt.Sprintf("%d.%s", ToInt(string(whole)), string(decimal)), 64)

	return f
}

// CleanTypeName will remove leading and trailing whitespace and leading asterisks.
func CleanTypeName(s string) string {
	return strings.TrimSuffix(strings.Trim(s, " "), "*")
}

func regexMatchedLines(matches map[int][]string) []int {
	keys := make([]int, len(matches))
	i := 0
	for k := range matches {
		keys[i] = k
		i++
	}
	sort.Ints(keys)
	return keys
}

func regexParseLines(re *regexp.Regexp, input Input) (map[int][]string, Input) {
	matches := make(map[int][]string)
	rest := make(Input)
	for i, line := range input {
		match := re.FindStringSubmatch(line)
		if len(match) == 0 {
			rest[i] = line
		} else {
			matches[i] = match
		}
	}
	return matches, rest
}

func StringsToInput(lines []string) Input {
	m := make(Input)
	for i, line := range lines {
		m[i] = line
	}
	return m
}

func StringToInput(s string) Input {
	s = strings.Replace(s, "\r", "", -1)
	return StringsToInput(strings.Split(s, "\n"))
}












// AssetList is the result from the asset parser
type AssetList struct {
	Items []AssetItem
	lines []int
}

// Name returns the parser name
func (r *AssetList) Name() string {
	return "assets"
}

// Lines returns the lines that this result is made from
func (r *AssetList) Lines() []int {
	return r.lines
}

// AssetItem is a single item parsed from an asset list
type AssetItem struct {
	Name          string
	Quantity      int64
	Volume        float64
	Group         string
	Category      string
	Size          string
	Slot          string
	MetaLevel     string
	TechLevel     string
	PriceEstimate float64
}

type AssetItemTest struct {
	Name          string
	Quantity      int64
}
//export Add
var reAssetList = regexp.MustCompile(strings.Join([]string{
	`^([\S\ ]*)`,                                 // Name
	`\t([` + bigNumberRegex + `*)`,               // Quantity
	`(?:\t([\S ]*))?`,                            // Group
	`(?:\t([\S ]*))?`,                            // Category
	`(?:\t(XLarge|Large|Medium|Small|))?`,        // Size
	`(?:\t(High|Medium|Low|Rigs|[\d ]*))?`,       // Slot
	`(?:\t(` + bigNumberRegex + `*) (m3|м\^3))?`, // Volume
	`(?:\t([\d]+|))?`,                            // meta level
	`(?:\t([\d]+|))?`,                            // tech level
	`(?:\t(` + bigNumberRegex + `+) ISK)?$`,      // price estimate
}, ""))

//export test
func test(i *C.char) {
	var j string
	j = C.GoString(i)
	fmt.Println(j)

}

//export ParseAssetsTest
func ParseAssetsTest(input_string *C.char) (*C.char) {

	input := StringToInput(C.GoString(input_string))


	assetList := &AssetList{}
	matches, rest := regexParseLines(reAssetList, input)
	assetList.lines = regexMatchedLines(matches)

	var items string

	for _, match := range matches {

		qty := ToInt(match[2])
		if qty == 0 {
			qty = 1
		}

		items = items + CleanTypeName(match[1]) + " _ " +  strconv.FormatInt(qty, 10) + "\n"

		/*assetList.Items = append(assetList.Items,
			AssetItem{
				Name:          CleanTypeName(match[1]),
				Quantity:      qty,
			})
			*/


		//fmt.Println("item", CleanTypeName(match[1]), qty)
	}
	//fmt.Println("items", items)
	//fmt.Println("rest", rest)
	_ = rest

	return C.CString(items)
}

//export ParseAssets
func ParseAssets(input_string *C.char) (ParserResult, Input) {

	input := StringToInput(C.GoString(input_string))
	fmt.Println(input)
	//time.Sleep(10000 * time.Millisecond)

	assetList := &AssetList{}
	matches, rest := regexParseLines(reAssetList, input)
	assetList.lines = regexMatchedLines(matches)

	for _, match := range matches {

		qty := ToInt(match[2])
		if qty == 0 {
			qty = 1
		}


		assetList.Items = append(assetList.Items,
			AssetItem{
				Name:          CleanTypeName(match[1]),
				Quantity:      qty,
				Group:         match[3],
				Category:      match[4],
				Size:          match[5],
				Slot:          match[6],
				Volume:        ToFloat64(match[7]),
				MetaLevel:     match[9],
				TechLevel:     match[10],
				PriceEstimate: ToFloat64(match[11]),
			})
	}

	sort.Slice(assetList.Items, func(i, j int) bool {
		return fmt.Sprintf("%v", assetList.Items[i]) < fmt.Sprintf("%v", assetList.Items[j])
	})
	fmt.Println("done", assetList)
	return assetList, rest
}

func main() {}
