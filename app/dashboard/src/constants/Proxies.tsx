import { ProxyHostSecurity } from "types/ProxyHosts";

export const proxyHostSecurity: { title: string; value: ProxyHostSecurity }[] =
  [
    {
      title: "Inbound's default",
      value: "inbound_default",
    },
    {
      title: "TLS",
      value: "tls",
    },
    {
      title: "None",
      value: "none",
    },
  ];

export const XTLSFlows = [
  { title: "none", value: "" },
  { title: "xtls-rprx-vision", value: "xtls-rprx-vision"},
];  

export const shadowsocksMethods = [
  "aes-128-gcm",
  "aes-256-gcm",
  "chacha20-poly1305",
];
