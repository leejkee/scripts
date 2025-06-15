# cgdisk xxx
# three partitions /boot [SWAP] /
mkfs.fat -F 32 /dev/nvme0n1p1
mkfs.btrfs -L ArchLinuxSystem /dev/nvme0n1p2

mount /dev/nvme0n1p2 /mnt

btrfs su cr /mnt/@
btrfs su cr /mnt/@home

umount /mnt

mount -o compress=zstd,subvol=@ /dev/nvme0n1p2 /mnt
mkdir -p /mnt/home
mount -o compress=zstd,subvol=@home /dev/nvme0n1p2 /mnt/home

mkdir -p /mnt/boot
mount /dev/nvme0n1p1 /mnt/boot
pacstrap -K /mnt base base-devel linux-lts linux-firmware git btrfs-progs timeshift neovim networkmanager openssh man sudo
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
hwclock --systohc
sed -i '178s/.//' /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" >> /etc/locale.conf
echo "val" >> /etc/hostname
echo "127.0.0.1 localhost" >> /etc/hosts
echo "::1       localhost" >> /etc/hosts
echo "127.0.1.1 val.localdomain val" >> /etc/hosts

useradd -mG wheel aude
passwd aude
EDITOR=nvim visudo

bootctl install

echo "default arch" >> /boot/loader/loader.conf
echo "timeout 5" >> /boot/loader/loader.conf
echo "console-mode 0" >> /boot/loader/loader.conf
echo "editor no" >> /boot/loader/loader.conf

echo -e "default arch.conf\ntimeout 5\nconsole-mode 0\neditor no" >> /boot/loader/loader.conf

touch /boot/loader/entries/arch.conf

echo -e "title GNU/Linux_arch\nlinux /vmlinuz-linux-lts\ninitrd /initramfs-linux-lts.img" >> /boot/loader/entries/arch.conf

blkid -o value -s PARTUUID /dev/nvme0n1p2 | xargs -I {} echo "options root=PARTUUID={} rootflags=subvol=@ rw" >> /boot/loader/entries/arch.conf

systemctl enable sshd
exit

umount -R /mnt

reboot

# 万一忘记装dhcpcd那些
echo -e  "[Match]\nName=ens33\n[Network]\nDHCP=yes" >> /etc/systemd/network/20-wired.network

sudo systemctl restart systemd-networkd
sudo systemctl restart systemd-resolved

sudo systemctl enable systemd-networkd
sudo systemctl enable systemd-resolved