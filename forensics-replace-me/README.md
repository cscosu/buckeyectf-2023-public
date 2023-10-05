# forensics-replace-me

`boot.img` is an android boot image file.

Only need to distribute `boot.img`.

Intended solve:
Find [mkbootimg_tools](https://github.com/xiaolu/mkbootimg_tools).

```sh
./mkboot boot.img out

ls out/ramdisk/res/images/charger/battery_fail.png
```

That image file has the flag.

## Flag

bctf{gr33n_r0b0t_ph0N3}
