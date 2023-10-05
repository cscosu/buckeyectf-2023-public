import Data.Bits
import Data.Char

shiftChar :: Char -> Int -> Char
shiftChar c offset
  | isAscii c = chr $ (ord c - ord ' ' + offset) `mod` 95 + ord ' '
  | otherwise = c

shiftString :: Int -> String -> String
shiftString offset = map (`shiftChar` offset)

allowedChars :: String
allowedChars = ['a' .. 'z'] ++ ['A' .. 'Z'] ++ ['0' .. '9'] ++ "_"

accumulateAndXOR :: String -> String
accumulateAndXOR input = accumulateAndXOR' input 0

accumulateAndXOR' :: String -> Int -> String
accumulateAndXOR' [] _ = []
accumulateAndXOR' (char : rest) acc =
  let newAcc = (acc + ord char) `mod` 128
      xorValue = newAcc `xor` ord char
      validChar = allowedChars !! (xorValue `mod` length allowedChars)
   in validChar : accumulateAndXOR' rest newAcc

addPositionToAscii :: String -> String
addPositionToAscii = addXsToString [0 ..]

addXsToString :: [Int] -> String -> String
addXsToString = zipWith (\pos char -> chr (ord char + pos))

simpleHash :: String -> String
simpleHash input = show $ foldr (\c acc -> acc * 31 + fromEnum c) 0 input

charToIndex :: Char -> Int
charToIndex c
  | isLower c = ord c - ord 'a' + 1
  | isUpper c = ord c - ord 'A' + 27
  | isDigit c = ord c - ord '0' + 53
  | otherwise = 0

multiplyChar :: Char -> Int -> Char
multiplyChar c offset
  | offset < 1 || offset > 62 = c
  | otherwise = indexToChar ((charToIndex c * offset) `mod` 62)

indexToChar :: Int -> Char
indexToChar idx
  | idx >= 1 && idx <= 26 = chr (ord 'a' + idx - 1)
  | idx >= 27 && idx <= 52 = chr (ord 'A' + idx - 27)
  | idx >= 53 && idx <= 62 = chr (ord '0' + idx - 53)
  | otherwise = ' '

multiplyString :: Int -> String -> String
multiplyString offset = map (`multiplyChar` offset)

step1 :: String -> String
step1 = addXsToString [-40, 8, -45, -43, -46] . addPositionToAscii

step2 :: String -> String
step2 = addXsToString [-33, 7, -24, 18, -17, 7] . reverse . accumulateAndXOR . addPositionToAscii

step3 :: String -> String
step3 = addXsToString [0, 6, -7, 0, 16, -45] . reverse . shiftString 1 . accumulateAndXOR . shiftString 16

step4 :: String -> String
step4 = addXsToString [0, -1, 27, 5, -9, -1] . multiplyString 8 . take 6 . simpleHash

-- bctf{7h475_3n0u6h_3moJi5_f0R_me}

main :: IO ()
main = do
  let f1 = replicate 5 '_'
  let f2 = replicate 6 '_'
  let f3 = replicate 6 '_'
  let f4 = replicate 6 '_'
  putStrLn $ concat ["bctf{", step1 f1, "_", step2 f2, "_", step3 f3, "_", step4 f4, "}"]
